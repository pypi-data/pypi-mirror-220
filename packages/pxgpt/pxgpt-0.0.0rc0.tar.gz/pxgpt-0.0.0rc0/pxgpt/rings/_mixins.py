from __future__ import annotations

from abc import ABC
from functools import cached_property
from multiprocessing import Pool
from pathlib import Path
from typing import TYPE_CHECKING, List, Mapping

from chromadb.config import Settings
from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredFileLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredURLLoader,
)
from langchain.vectorstores import Chroma, SKLearnVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

if TYPE_CHECKING:
    from langchain.embeddings.base import Embeddings
    from langchain.docstore.document import Document


class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if "text/html content not found in email" in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"] = "text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc


class MyURLLoader(UnstructuredFileLoader):
    """Load the content with the URL in a file"""

    def load(self) -> List[Document]:
        urls = Path(self.file_path).read_text().strip().splitlines()
        loader = UnstructuredURLLoader(
            urls,
            headers={"User-Agent": "Mozilla/5.0", "ssl_verify": False},
        )
        return loader.load()


LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    ".url": (MyURLLoader, {}),
    ".urls": (MyURLLoader, {}),
}


def load_single_document(file_path: str) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1]
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")


class ChromaIngestorMixin(ABC):
    """Ingest the documents into the database.

    Part of the code is borrowed from
    https://github.com/imartinez/privateGPT/blob/main/ingest.py
    by Ivan Martinez.

    Check the LICENSE file for the license of the original code.

    There is a bug with chroma, that each time that it may generte a different
    uuid, so that an empty vector will be returned for the persisted document.
    See: https://github.com/hwchase17/langchain/issues/3011

    So we use SKLearnVectorStore instead.
    """

    @cached_property
    def persist_directory(self) -> str:
        """Get the persist directory"""
        source_directory = Path(self.config.ingest.source_directory)
        if not source_directory.exists():
            raise ValueError(
                f"Source directory {source_directory} does not exist"
            )

        if self.config.ingest.persist_directory is None:
            pd = Path(self.config.ingest.source_directory).joinpath(
                f".pxgpt-{self.config.model.type.lower()}-db"
            )
            pd.mkdir(exist_ok=True)
            pd = str(pd)
        else:
            pd = self.config.ingest.persist_directory

        return pd

    @property
    def embeddings(self) -> Embeddings:
        """The embeddings"""
        raise NotImplementedError

    def db(self, texts: List[Document] | None = None) -> Chroma:
        """Get the database"""
        settings = Settings(
            chroma_db_impl=self.config.ingest.chroma_db_impl,
            persist_directory=self.persist_directory,
            anonymized_telemetry=self.config.ingest.chroma_anonymized_telemetry,
        )
        if texts is None:
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                client_settings=settings,
            )

        return Chroma.from_documents(
            texts,
            persist_directory=self.persist_directory,
            embedding=self.embeddings,
            client_settings=settings,
        )

    def get_docs(self) -> Mapping[str, List[Mapping[str, str]]]:
        """Get the ingested files"""
        out = {"ingested": [], "pending": []}
        collection = self.db().get()

        ingested = [
            Path(metadata["source"]).resolve()
            for metadata in collection["metadatas"]
        ]
        persist_directory = Path(self.persist_directory).resolve()
        source_directory = Path(self.config.ingest.source_directory).resolve()
        for doc in source_directory.rglob("*"):
            if (
                doc.name.startswith(".")
                or doc.is_dir()
                or doc.is_relative_to(persist_directory)
                or doc.suffix in (".parquet", ".bin", ".pkl")
            ):
                continue
            if doc in ingested:
                out["ingested"].append({"name": doc.name, "path": str(doc)})
            else:
                out["pending"].append({"name": doc.name, "path": str(doc)})

        return out

    def load_documents(self, ignored_files: List[str]) -> List[Document]:
        """Loads all documents from the source documents directory, ignoring
        specified files
        """
        status = []
        all_files = set()
        source_dir = Path(self.config.ingest.source_directory)

        for ext in LOADER_MAPPING:
            all_files = all_files | set(
                (str(p) for p in source_dir.rglob(f"*{ext}"))
            )

        filtered_files = all_files - set(ignored_files)

        if not status:
            status = [0, len(filtered_files)]  # loaded, total

        with Pool(processes=self.config.ingest.n_workers or None) as pool:
            results = []
            for docs in pool.imap_unordered(
                load_single_document, filtered_files
            ):
                results.extend(list(docs))
                status[0] += 1
                self.logger.info("Loaded %s/%s documents", *status)

        return results

    def process_documents(
        self,
        ignored_files: List[str] | None = None,
    ) -> List[Document]:
        """Load documents and split in chunks"""
        ignored_files = ignored_files or []

        self.logger.info(
            "Loading documents from %s",
            self.config.ingest.source_directory,
        )
        documents = self.load_documents(ignored_files)
        if not documents:
            self.logger.warning("No new documents to load")
            return []

        self.logger.info("Loaded %s new documents", len(documents))
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.ingest.chunk_size,
            chunk_overlap=self.config.ingest.chunk_overlap,
        )
        texts = text_splitter.split_documents(documents)
        self.logger.info(
            "Split into {%s} chunks of text (max. {%s} tokens each)",
            len(texts),
            self.config.ingest.chunk_size,
        )
        return texts

    def does_vectorstore_exist(self) -> bool:
        """Checks if vectorstore exists"""
        persist_directory = Path(self.persist_directory)

        if (
            not persist_directory.joinpath("index").exists()
            or not persist_directory.joinpath(
                "chroma-collections.parquet"
            ).exists()
            or not persist_directory.joinpath(
                "chroma-embeddings.parquet"
            ).exists()
        ):
            return False

        list_index_files = list(
            persist_directory.joinpath("index").glob("*.bin")
        )
        list_index_files.extend(
            persist_directory.joinpath("index").glob("*.pkl")
        )
        # At least 3 documents are needed in a working vectorstore
        return len(list_index_files) > 3

    def ingest(self, force: bool = False) -> None:
        if self.does_vectorstore_exist():
            # Update and store locally vectorstore
            self.logger.info(
                "Appending to existing vectorstore at %s",
                self.persist_directory,
            )
            db = self.db()
            if force:
                self.logger.info(
                    "Clear current collection for force ingestion"
                )
                db._collection.delete()

            collection = db.get()

            texts = self.process_documents(
                # Ignore already ingested files
                [metadata["source"] for metadata in collection["metadatas"]],
            )

            if not texts:
                return

            self.logger.info("Creating embeddings. May take some minutes...")
            db.add_documents(texts)
        else:
            # Create and store locally vectorstore
            self.logger.info(
                "Creating new vectorstore at %s",
                self.persist_directory,
            )
            texts = self.process_documents()

            if not texts:
                return

            self.logger.info("Creating embeddings. May take some minutes...")
            db = self.db(texts)

        db.persist()
        db = None

        self.logger.info("Ingestion complete!")


class SKLearnInvestorMixin(ChromaIngestorMixin, ABC):

    @property
    def persist_path(self) -> str:
        return str(Path(self.persist_directory).joinpath("db.parquet"))

    def db(self, texts: List[Document] | None = None) -> SKLearnVectorStore:
        """Get the database"""

        if texts:
            vs = SKLearnVectorStore.from_documents(
                documents=texts,
                persist_path=self.persist_path,
                embedding=self.embeddings,
                serializer="parquet",
            )
        else:
            vs = SKLearnVectorStore(
                embedding=self.embeddings,
                persist_path=self.persist_path,
                serializer="parquet",
            )

        return vs

    def get_docs(self) -> Mapping[str, List[Mapping[str, str]]]:
        """Get the ingested files"""
        out = {"ingested": [], "pending": []}
        db = self.db()

        ingested = [
            Path(metadata["source"]).resolve()
            for metadata in db._metadatas
        ]
        persist_directory = Path(self.persist_directory).resolve()
        source_directory = Path(self.config.ingest.source_directory).resolve()
        for doc in source_directory.rglob("*"):
            if (
                doc.name.startswith(".")
                or doc.is_dir()
                or doc.is_relative_to(persist_directory)
                or doc.suffix in (".parquet", ".bin", ".pkl")
            ):
                continue
            if doc in ingested:
                out["ingested"].append({"name": doc.name, "path": str(doc)})
            else:
                out["pending"].append({"name": doc.name, "path": str(doc)})

        return out

    def does_vectorstore_exist(self) -> bool:
        """Checks if vectorstore exists"""
        persist_path = Path(self.persist_path)
        return persist_path.exists()

    def ingest(self, force: bool = False) -> None:
        if self.does_vectorstore_exist():
            # Update and store locally vectorstore
            self.logger.info(
                "Appending to existing vectorstore at %s",
                self.persist_path,
            )
            if force:
                Path(self.persist_path).unlink()

            db = self.db()

            texts = self.process_documents(
                # Ignore already ingested files
                [metadata["source"] for metadata in db._metadatas],
            )

            if not texts:
                return

            self.logger.info("Creating embeddings. May take some minutes...")
            db.add_documents(texts)
        else:
            # Create and store locally vectorstore
            self.logger.info(
                "Creating new vectorstore at %s",
                self.persist_directory,
            )
            texts = self.process_documents()

            if not texts:
                return

            self.logger.info("Creating embeddings. May take some minutes...")
            db = self.db(texts)

        db.persist()
        db = None

        self.logger.info("Ingestion complete!")
