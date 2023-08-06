"""Provides some special callbacks for streaming and other purposes."""

from __future__ import annotations

import sys
from contextlib import suppress
from typing import TYPE_CHECKING, Any, Dict, List
from uuid import UUID, uuid4

from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import LLMResult

if TYPE_CHECKING:
    from langchain.schema.output import LLMResult


class DocumentStreamingStdOutCallbackHandler(StreamingStdOutCallbackHandler):
    """A callback handler inherited from the StreamingStdOutCallbackHandler
    but prints the source documents.

    This callback handler can be called by both a real chain or called pseudoly
    after parsing the output from the spawned process.
    """

    def on_llm_new_token(
        self, token: str, tags: List[str], **kwargs: Any
    ) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        # Ignore the qmodel, which is used for condense the query.
        if "qmodel" in tags:
            return

        return super().on_llm_new_token(token, **kwargs)

    def on_chain_end(
        self, outputs: Dict[str, Any] | str, **kwargs: Any
    ) -> None:
        """Run when chain ends running."""
        if isinstance(outputs, str) and outputs.startswith(
            "@source_documents:"
        ):
            # from pseduo call
            sources = outputs[len("@source_documents:") :].split(";")
            sys.stdout.write("\n\nSources:")
            for source in sources:
                sys.stdout.write(f"\n- {source}")
            sys.stdout.flush()

        elif "source_documents" in outputs:
            # from real chain call
            sys.stdout.write("\n\nSources:")
            sources = set(
                [doc.metadata["source"] for doc in outputs["source_documents"]]
            )
            for source in sources:
                sys.stdout.write(f"\n- {source}")
            sys.stdout.flush()


class ZzzCallbackHandler(BaseCallbackHandler):
    """A callback handler for the zzz command.

    It prints to stdout, and then the message will be parsed by the parent
    process, and sent to the real callback handlers.
    """

    def _send(
        self, func: str, msg: str | None = None, tags: List[str] = []
    ) -> None:
        """Send message to stdout

        Args:
            func: The callback handler function name
            msg: The message
            tags: The tags of the chain
        """
        msg = msg or ""
        msg = msg.replace("\n", "\\n")
        tag = tags[0] if tags else ""
        sys.stdout.write(f"@{func}:{tag}:{msg}\n")
        sys.stdout.flush()

    def on_llm_new_token(self, token: str, **kwargs) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""
        self._send("on_llm_new_token", token, tags=kwargs.get("tags", []))

    def on_llm_end(self, response: LLMResult, **kwargs) -> Any:
        """Run when LLM ends running."""
        self._send("on_llm_end", tags=kwargs.get("tags", []))

    def on_llm_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> Any:
        """Run when LLM errors."""
        self._send("on_llm_error", str(error), tags=kwargs.get("tags", []))

    def on_tool_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> Any:
        """Run when tool errors."""
        self._send("on_tool_error", str(error), tags=kwargs.get("tags", []))

    def on_chain_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> Any:
        """Run when chain errors."""
        self._send("on_chain_error", str(error), tags=kwargs.get("tags", []))

    def on_retriever_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> Any:
        """Run when retriever errors."""
        self._send(
            "on_retriever_error", str(error), tags=kwargs.get("tags", [])
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> Any:
        """Run when chain ends running."""
        msg = ""
        if "source_documents" in outputs:
            sources = set(
                [doc.metadata["source"] for doc in outputs["source_documents"]]
            )
            msg = ";".join(sources)
            msg = f"@source_documents:{msg}"
        self._send("on_chain_end", msg, tags=kwargs.get("tags", []))


class StreamingWebsocketCallbackHandler(AsyncCallbackHandler):
    """A callback handler for communicating with the websocket"""

    def __init__(self, ws) -> None:
        """Initialize the callback handler and the websocket"""
        super().__init__()
        self.ws = ws

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        with suppress(BrokenPipeError):
            await self.ws.send_json(
                {
                    "event": "responding",
                    "message": token,
                }
            )

    async def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Run when LLM ends running."""
        await self.ws.send_json(
            {
                "event": "query_finished",
            }
        )

    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain ends running."""
        if run_id is None:  # pseudo call
            run_id = uuid4()
        return await super().on_chain_end(outputs, run_id=run_id, **kwargs)

    async def on_llm_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> None:
        """Run when LLM errors."""
        await self.ws.send_json(
            {
                "event": "lc_error",
                "type": "llm",
                "error": str(error),
            }
        )

    async def on_tool_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> None:
        """Run when tool errors."""
        await self.ws.send_json(
            {
                "event": "lc_error",
                "type": "tool",
                "error": str(error),
            }
        )

    async def on_chain_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> None:
        """Run when chain errors."""
        await self.ws.send_json(
            {
                "event": "lc_error",
                "type": "chain",
                "error": str(error),
            }
        )

    async def on_retriever_error(
        self, error: Exception | KeyboardInterrupt, **kwargs
    ) -> None:
        """Run when retriever errors."""
        await self.ws.send_json(
            {
                "event": "lc_error",
                "type": "retriever",
                "error": str(error),
            }
        )
