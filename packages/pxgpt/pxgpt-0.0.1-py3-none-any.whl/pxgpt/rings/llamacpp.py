"""Provides ring for the LlamaCpp model."""
from __future__ import annotations
from pathlib import Path

from typing import TYPE_CHECKING, Any, List, Mapping
from langchain.callbacks.base import BaseCallbackHandler
from langchain.embeddings import LlamaCppEmbeddings
from langchain.llms import LlamaCpp
from py.io import StdCaptureFD

from .base import NoAsyncSupportRing

if TYPE_CHECKING:
    from langchain.embeddings.base import Embeddings


class LlamaCppRing(NoAsyncSupportRing):

    MODEL = LlamaCpp

    @property
    def embeddings(self) -> Embeddings:
        """Return the embeddings for the model."""
        args = {"model_path": self.config.model.model_path}
        args.update(self.config.embeddings)
        return LlamaCppEmbeddings(**args)

    def query(
        self,
        query: str,
        history: Path,
        callbacks: List[BaseCallbackHandler] | BaseCallbackHandler,
    ) -> Mapping[str, Any]:
        """Query the model.

        Capture the logs of the model
        """
        capture = StdCaptureFD(out=False, err=True, in_=False)
        ret = super().query(query, history, callbacks)
        _, err = capture.reset()
        for line in err.splitlines():
            line = line.strip()
            if not line:
                continue
            if (
                line.startswith("llama_")
                or line.startswith("llama.cpp")
                or ("AVX" in line and "FMA" in line)
            ):
                self.logger.debug(line)
            else:
                self.logger.error(line)

        return ret
