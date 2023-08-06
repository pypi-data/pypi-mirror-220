"""Provides ring for the LlamaCpp model."""
from __future__ import annotations

from typing import TYPE_CHECKING
from langchain.embeddings import LlamaCppEmbeddings
from langchain.llms import LlamaCpp

from .base import NoAsyncSupportRing

if TYPE_CHECKING:
    from langchain.embeddings.base import Embeddings


class LlamaCppRing(NoAsyncSupportRing):

    MODEL = LlamaCpp

    @property
    def embeddings(self) -> Embeddings:
        return LlamaCppEmbeddings(**self.config.embeddings)

    # def _create_llm(self) -> LlamaCpp:
    #     """Create the LLM object"""
    #     llm = super()._create_llm()
    #     # https://github.com/ggerganov/llama.cpp/issues/999
    #     llm.client.verbose = False
    #     return llm
