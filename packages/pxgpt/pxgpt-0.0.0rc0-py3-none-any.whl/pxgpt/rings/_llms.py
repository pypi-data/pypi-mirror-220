from __future__ import annotations

from typing import List

from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun


class EchoLLM(LLM):
    """An LLM that echoes the prompt.

    It is used when you don't want to condense your question with chat history.
    Helpful for small models.
    """

    @property
    def _llm_type(self) -> str:
        """Return the LLM type."""
        return "echo"

    def _call(
        self,
        prompt: str,
        stop: List[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
    ) -> str:
        """Echo the prompt."""
        if stop is not None:
            raise ValueError("EchoLLM does not support stop.")
        return prompt
