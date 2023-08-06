"""Provides ring for GPT4All."""
from __future__ import annotations

from typing import TYPE_CHECKING
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import GPT4All

from .base import NoAsyncSupportRing

if TYPE_CHECKING:
    from langchain.embeddings.base import Embeddings


class GPT4AllRing(NoAsyncSupportRing):

    MODEL = GPT4All

    @property
    def embeddings(self) -> Embeddings:
        return HuggingFaceEmbeddings(**self.config.embeddings)
