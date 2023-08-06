"""Provides ring for GPT4All."""
from __future__ import annotations
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from typing import TYPE_CHECKING
from langchain.embeddings import GPT4AllEmbeddings
from langchain.llms import GPT4All

from .base import NoAsyncSupportRing

if TYPE_CHECKING:
    from langchain.embeddings.base import Embeddings


class GPT4AllRing(NoAsyncSupportRing):

    MODEL = GPT4All

    @property
    def embeddings(self) -> Embeddings:
        args = self.config.embeddings or {}
        # Hide Found model file at  ....
        with StringIO() as buf, redirect_stdout(buf):
            model = GPT4AllEmbeddings(**args)
            out = buf.getvalue()

        for line in out.splitlines():
            self.logger.debug(line)

        return model

    @property
    def model_args(self):
        out = super().model_args
        # Use model to specify the model path
        if "model_path" in out:
            del out["model_path"]
        return out
