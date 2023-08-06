"""Provides the base ring class for different models and chains"""
from __future__ import annotations
import asyncio

import json
import re
import sys
import textwrap
from abc import ABC
from contextlib import contextmanager
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Type

from langchain.chains import (
    ConversationChain,
    ConversationalRetrievalChain,
    LLMChain,
)
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.schema.messages import messages_from_dict, messages_to_dict
from langchain.prompts.prompt import PromptTemplate

from ._llms import EchoLLM
from ._mixins import SKLearnInvestorMixin
from ..logger import get_logger

if TYPE_CHECKING:
    from diot import Diot
    from langchain.llms.base import LLM
    from langchain.chains.base import Chain


class DocumentRetrievalBufferMemory(ConversationBufferMemory):
    """Make ConversationBufferMemory work with return_source_documents=True
    See https://github.com/hwchase17/langchain/issues/5630
    """

    def save_context(
        self, inputs: Dict[str, Any], outputs: Dict[str, str]
    ) -> None:
        return super().save_context(inputs, {"response": outputs["answer"]})


class BaseRing(SKLearnInvestorMixin, ABC):
    """Rings are classes that wrap around LLM and Chains from different
    langchain, based on different model types.

    It assembles the LLM and Chain objects, and provides a unified interface
    for the query, with or without documents.

    Args:
        config: A Diot object that contains all the configuration
        logger: A logger object
        init_llm: Whether to initialize the LLMs in the constructor
    """

    MODEL: LLM | None = None

    def __init__(
        self,
        config: Diot,
        profile: str,
        init_llm: bool = True,
    ) -> None:
        """Initialize the ring"""
        self.config = config
        self.profile = profile
        self.logger = get_logger(config.log_level)

        if init_llm:
            self.llm = self._create_llm()
            self.qllm = self._create_qllm()
        else:
            self.llm = None
            self.qllm = None

        if self.config.ingest.source_directory:
            self.logger.info("Entering document retrieval mode")
        else:
            self.logger.info("Entering chat mode")

    @property
    def model_args(self):
        """Get the model arg that will be passed to the model"""
        args = {k: v for k, v in self.config.model.items() if k != "type"}
        args.update({"streaming": True, "verbose": False})
        return args

    @property
    def qmodel(self) -> Type[LLM]:
        """Get the qmodel class

        When qmodel is not found in config, then class of model will be used.
        """
        if "qmodel" not in self.config:
            return None

        qm = self.config.qmodel.get("type", self.config.model.type)
        if qm == self.config.model.type:
            return None

        if qm == "Echo":
            return EchoLLM
        if qm == "OpenAI":
            from langchain.llms import OpenAI

            return OpenAI
        if qm == "ChatOpenAI":
            from langchain.chat_models import ChatOpenAI

            return ChatOpenAI
        if qm == "GPT4All":
            from langchain.llms import GPT4All

            return GPT4All
        if qm == "LlamaCpp":
            from langchain.llms import LlamaCpp

            return LlamaCpp

        raise ValueError(f"Unsupported qmodel type '{qm}'")

    @property
    def qmodel_args(self):
        """Get the qmodel arg that will be passed to the question condenser"""
        qargs = self.config.get("qmodel", {}).copy()
        qargs = {k: v for k, v in qargs.items() if k != "type"}
        qargs.update(
            {"streaming": False, "verbose": False, "tags": ["qmodel"]}
        )
        return qargs

    def _create_llm(self) -> LLM:
        """Create the LLM object

        Custom rings should override this method if MODEL is not set
        """
        self.logger.info("Creating LLM (%s)", self.config.model.type)
        if self.MODEL is None:
            raise NotImplementedError

        return self.MODEL(**self.model_args)

    def _create_qllm(self) -> LLM | None:
        """Create the LLM for question condensing

        When config.ingest.source_directory is not set, this method will not be
        called.

        When self.qmodel is None, self.llm is copied, with some fields updated,
        including steaming=False, verbose=False, callbacks=None,
        tags=["qmodel"] and metadata={}.
        """
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

        return self.qmodel(**self.qmodel_args)

    def _create_chat_chain(self) -> Chain:
        """Create the chat chain object for chatting only, without documents

        A ConversationChain object is created.
        Custom rings can override this method to create a different chain.
        """
        self.logger.debug("Creating chat chain")
        prompt_template = textwrap.dedent(
            """
            The following is a friendly conversation between a human and an AI.
            The AI is talkative and provides lots of specific details from its
            context. If the AI does not know the answer to a question,
            it truthfully says it does not know. After answering a question,
            the AI should NOT ask follow-up questions, followed by the "Human:"
            prefix.

            Previous conversation:
            {history}

            Current conversation:
            Human: {input}
            AI:"""
        ).lstrip()
        prompt = PromptTemplate.from_template(prompt_template)
        return ConversationChain(llm=self.llm, prompt=prompt)

    def _create_retrieval_chain(self) -> Chain:
        """Create the retrieval chain object for document retrieval

        A ConversationalRetrievalChain object is created.
        Custom rings can override this method to create a different chain.
        If you want to use the default chain, you can choose to use a
        different question condenser, or even not to use one. Then you must
        be aware that the "qmodel" section in the config will be ignored.
        """
        self.logger.debug("Creating retrieval chain")
        main_chain = load_qa_chain(self.llm, verbose=False)
        cqp = textwrap.dedent(
            """
            Given the following conversation and a follow up question,
            rephrase the follow up question to be a standalone question,
            in its original language. The new question should be
            grammatically correct and semantically similar to the original
            question. If the chat history is not enough, you can keep the
            original question as is.

            Chat History:
            {chat_history}

            Follow Up Input: {question}
            Standalone question:"""
        ).lstrip()
        condense_question_chain = LLMChain(
            llm=self.qllm,
            prompt=PromptTemplate.from_template(cqp),
            verbose=False,
            tags=["qchain"],
        )
        return ConversationalRetrievalChain(
            retriever=self.db().as_retriever(
                search_kwargs={"k": self.config.ingest.target_source_chunks}
            ),
            combine_docs_chain=main_chain,
            question_generator=condense_question_chain,
            return_source_documents=True,
            memory=DocumentRetrievalBufferMemory(memory_key="chat_history"),
            get_chat_history=lambda x: x,
        )

    @cached_property
    def chain(self):
        """The chain object for chatting or document retrieval"""
        if self.config.ingest.source_directory:
            return self._create_retrieval_chain()
        return self._create_chat_chain()

    @contextmanager
    def _history_context(self, history: Path):
        """A context manager that loads and saves history

        With it, when subclasses override the _chat_chain_call and
        _retrieval_chain_call methods, they don't need to worry about
        loading and saving history.

        Args:
            history: The history file path
        """
        with history.open() as f:
            data = json.load(f)

        memory = self.chain.memory
        if self.config.history_into_memory:
            messages = messages_from_dict(data.get("history", []))
            memory.chat_memory = ChatMessageHistory(messages=messages)

        if not self.chain.metadata:
            self.chain.metadata = {}

        yield

        if self.config.history_into_memory:
            data["history"] = messages_to_dict(memory.chat_memory.messages)
        else:
            data["history"].extend(
                messages_to_dict(memory.chat_memory.messages)
            )

        with history.open("w") as f:
            json.dump(data, f, indent=2)

    def _chat_chain_call(
        self,
        query: str,
        callbacks: List[BaseCallbackHandler],
    ) -> Mapping[str, Any]:
        """Query the model with a string

        Note that if you have different input keys for you chain, you should
        override this method.
        """
        self.logger.debug("Chat calling: %r", query)
        return self.chain(
            {"input": query},
            callbacks=callbacks,
            return_only_outputs=True,
        )

    async def _a_chat_chain_call(
        self,
        query: str,
        callbacks: List[BaseCallbackHandler],
    ) -> Mapping[str, Any]:
        """Query the model with a string asynchronously

        Note that if you have different input keys for you chain, you should
        override this method.
        """
        self.logger.debug("Chat calling asynchronously: %r", query)
        return await self.chain.acall(
            {"input": query},
            callbacks=callbacks,
            return_only_outputs=True,
        )

    def _retrieval_chain_call(
        self,
        query: str,
        callbacks: List[BaseCallbackHandler],
    ) -> Mapping[str, Any]:
        """Query the model with a string

        Note that if you have different input keys for you chain, you should
        override this method.
        """
        self.logger.debug("Retrieval calling: %r", query)
        return self.chain(
            {"question": query, "chat_history": []},
            callbacks=callbacks,
            return_only_outputs=True,
        )

    async def _a_retrieval_chain_call(
        self,
        query: str,
        callbacks: List[BaseCallbackHandler],
    ) -> Mapping[str, Any]:
        """Query the model with a string asynchronously

        Note that if you have different input keys for you chain, you should
        override this method.
        """
        self.logger.debug("Retrieval calling asynchronously: %r", query)
        return await self.chain.acall(
            {"question": query, "chat_history": []},
            callbacks=callbacks,
            return_only_outputs=True,
        )

    def query(
        self,
        query: str,
        history: Path,
        callbacks: List[BaseCallbackHandler] | BaseCallbackHandler,
    ) -> Mapping[str, Any]:
        """Query the model with a string"""
        if isinstance(callbacks, BaseCallbackHandler):
            callbacks = [callbacks]

        self.logger.debug("Querying: %r", query)
        with self._history_context(history):
            if self.config.ingest.source_directory:
                return self._retrieval_chain_call(query, callbacks)
            return self._chat_chain_call(query, callbacks)

    async def a_query(
        self,
        query: str,
        history: Path,
        callbacks: List[BaseCallbackHandler] | BaseCallbackHandler,
    ) -> Mapping[str, Any]:
        """Query the model with a string asynchronously"""
        if isinstance(callbacks, BaseCallbackHandler):
            callbacks = [callbacks]

        self.logger.debug("Querying asynchronously: %r", query)
        with self._history_context(history):
            if self.config.ingest.source_directory:
                return await self._a_retrieval_chain_call(query, callbacks)
            return await self._a_chat_chain_call(query, callbacks)


async def _pseduo_callbacks_call(
    callbacks: List[BaseCallbackHandler],
    func: str,
    *args: Any,
    **kwargs: Any,
) -> None:
    """Call the passed-in callback handlers in a pseudo way

    This is used in the workaround for async not supported by some chains/llms.
    The information are gathered from stdout of the spawned process, so
    most of the information are lost. So you pass in the callbacks, pay
    attention that if they use some information that are not supported.

    Args:
        callbacks: The callback handlers, could be either sync or async
        func: The function name to call
        args: The args to pass to the function
        kwargs: The kwargs to pass to the function
    """
    for cb in callbacks:
        called = getattr(cb, func)(*args, **kwargs)
        # if called is a coroutine, await it
        if hasattr(called, "__await__"):
            await called


class NoAsyncSupportRing(BaseRing, ABC):
    """A ring with a workaround for async not supported by some chains/llms.

    Not that with the workaround, we are not able to get the final results,
    everything has to be done with the callbaks.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the ring"""
        super().__init__(*args, **kwargs)
        self.spawned = None

    def __del__(self):
        """Terminate the spawned process"""
        if self.spawned:
            self.logger.debug("Terminating spawned process")
            self.spawned.terminate()
            self.spawned = None

    async def _a_call(
        self,
        query: str,
        history: Path,
        callbacks: List[BaseCallbackHandler],
    ) -> None:
        """Query the model in a spawned process calling the zzz subcommand

        Args:
            query: The query
            history: The history file path
            callbacks: The callback handlers
        """
        if not self.spawned:
            self.logger.debug("Spawning process")
            self.spawned = await asyncio.create_subprocess_exec(
                sys.executable,
                "-m",
                "pxgpt",
                "zzz",
                "--profile",
                self.profile,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

        conversation = history.stem
        # pass the conversation
        self.spawned.stdin.write(
            f"@on_conversation_input:{conversation}\n".encode()
        )
        self.spawned.stdin.write(b"@on_input_end\n")
        # pass the query
        for line in query.splitlines():
            self.spawned.stdin.write(f"@on_query_input:{line}\n".encode())
        self.spawned.stdin.write(b"@on_input_end\n")
        await self.spawned.stdin.drain()

        # parse the output, like on_llm_new_token::token
        regex = re.compile(r"^@on_([\w_]+):([\w_]*):(.*)")
        async for line in self.spawned.stdout:
            line = line.decode().rstrip("\n")
            match = regex.match(line)
            if not match:
                # ignore unmatched lines
                continue

            func, tag, msg = match.groups()
            msg = msg.replace("\\n", "\n")

            # logging messages
            if func == "log":
                getattr(self.logger, tag.lower())(f"[spawned] {msg}")
                continue

            tags = [tag] if tag else []
            func = f"on_{func}"
            await _pseduo_callbacks_call(callbacks, func, msg, tags=tags)
            # main chain (without tags) ends
            if func == "on_chain_end" and not tag:
                break

    async def a_query(
        self,
        query: str,
        history: Path,
        callbacks: List[BaseCallbackHandler] | BaseCallbackHandler,
    ) -> Mapping[str, Any]:
        """Query the model with a string asynchronously"""
        if isinstance(callbacks, BaseCallbackHandler):
            callbacks = [callbacks]

        self.logger.debug("Querying with async workaround: %r", query)
        # History will be saved by subprocess
        await self._a_call(query, history, callbacks)
