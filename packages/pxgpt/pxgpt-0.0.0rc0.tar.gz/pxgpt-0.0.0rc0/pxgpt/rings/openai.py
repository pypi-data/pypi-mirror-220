"""Provides ring for OpenAI models, such as text-davinci-***."""
from __future__ import annotations

from typing import TYPE_CHECKING, Mapping
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.llms.base import LLM

from .base import BaseRing

if TYPE_CHECKING:
    from langchain.embeddings.base import Embeddings


class OpenAIRing(BaseRing):

    MODEL = OpenAI

    @property
    def credentials(self) -> Mapping[str, str]:
        return {
            key: val
            for key, val in self.config.credentials.items()
            if key in (
                "openai_api_key",
                "openai_api_base",
                "openai_organization",
                "openai_proxy",
            )
        }

    @property
    def embeddings(self) -> Embeddings:
        return OpenAIEmbeddings(**self.credentials, **self.config.embeddings)

    def _create_llm(self) -> LLM:
        """Create the LLM object, pass the credentials to it"""
        self.logger.info("Creating LLM (%s)", self.config.model.type)

        return self.MODEL(**self.model_args, **self.credentials)

    def _create_qllm(self) -> LLM | None:
        """Create the QLLM object, pass the credentials to it"""
        if not self.config.ingest.source_directory:
            return None

        qmodel_name = (
            self.config.model.type
            if self.qmodel is None
            else self.qmodel.__name__
        )
        self.logger.info("Creating QLLM (%s)", qmodel_name)
        if self.qmodel is None:
            return self.llm.copy(
                include=set(self.llm.__fields__),
                update={
                    "streaming": False,
                    "verbose": False,
                    "callbacks": None,
                    "tags": ["qmodel"],
                    "metadata": {},
                },
            )

        if "OpenAI" in qmodel_name:
            return self.qmodel(**self.qmodel_args, **self.credentials)

        return self.qmodel(**self.qmodel_args)
