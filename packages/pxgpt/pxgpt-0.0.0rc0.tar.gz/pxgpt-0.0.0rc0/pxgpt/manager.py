"""Provides the Manager class"""
from __future__ import annotations

import time
import json

from functools import lru_cache
from pathlib import Path
from typing import Any, List, Mapping
from langchain.callbacks.base import BaseCallbackHandler

from diot import FrozenDiot
from simpleconf import ProfileConfig

from .config import config
from .logger import get_logger
from .rings.base import NoAsyncSupportRing


class Manager:
    """The ring manager

    Manages the rings and histories.
    """

    def __init__(self, profile: str, serving: bool = False):
        """Initialize the manager

        Args:
            profile: The profile
            serving: Whether the manager is used for serving
                Primarily used for determining whether to initialize the LLMs
                for those rings that do not support async. Since we don't need
                to initialize the LLMs, as they will be initialized by the
                spawned process.
        """
        old_profile = ProfileConfig.current_profile(config)
        if old_profile != profile:
            ProfileConfig.use_profile(config, profile)

        self.config = FrozenDiot(ProfileConfig.detach(config))
        self.profile = profile
        self.logger = get_logger(self.config.log_level)
        if old_profile != profile:
            self.logger.info("Switched profile to %s", profile)

        self.ring = self._create_ring(serving)

    def close(self):
        """Close the manager"""
        del self.ring

    def _create_ring(self, serving: bool):
        """Create the ring"""
        # Avoid changes to the config
        model_type = self.config.model.type

        def should_init_llm(ring_class):
            return not serving or not issubclass(
                ring_class, NoAsyncSupportRing
            )

        if model_type == "GPT4All":
            from .rings.gpt4all import GPT4AllRing

            return GPT4AllRing(
                self.config,
                self.profile,
                init_llm=should_init_llm(GPT4AllRing),
            )
        if model_type == "LlamaCpp":
            from .rings.llamacpp import LlamaCppRing

            return LlamaCppRing(
                self.config,
                self.profile,
                init_llm=should_init_llm(LlamaCppRing),
            )
        if model_type == "OpenAI":
            from .rings.openai import OpenAIRing

            return OpenAIRing(
                self.config, self.profile, init_llm=should_init_llm(OpenAIRing)
            )
        if model_type == "ChatOpenAI":
            from .rings.chatopenai import ChatOpenAIRing

            return ChatOpenAIRing(
                self.config,
                self.profile,
                init_llm=should_init_llm(ChatOpenAIRing),
            )
        else:
            raise ValueError(f"Unknown ring: {model_type}")

    def get_docs(self) -> Mapping[str, List[Mapping[str, str]]]:
        """Get the documents"""
        return self.ring.get_docs()

    def ingest(self, force: bool = False) -> None:
        """Ingest the documents"""
        self.ring.ingest(force=force)

    def get_histories(
        self, include_title: bool = False
    ) -> List[str | Mapping[str, Any]]:
        """Get the list of histories

        Args:
            include_title: Whether to include the title of the history
                If True, each element of the output list will be a dict
                with the keys `name` and `title`. Otherwise, it will be
                a string with the name of the history.

        Returns:
            List[str | Mapping[str, Any]]: The list of histories
        """
        history_dir = (
            Path(self.config.history_directory)
            .joinpath(self.profile)
            .expanduser()
        )

        return [
            hfile.stem
            if not include_title
            else {
                "name": hfile.stem,
                "title": self.history_title(
                    hfile.stem, fallback=True, add_date=False
                ),
            }
            for hfile in sorted(
                history_dir.glob("*.json"),
                reverse=True,
                key=lambda x: x.stat().st_ctime,
            )
        ]

    @lru_cache()
    def history_file(self, history: str, title: str | None = None) -> Path:
        """Get the path to a history file

        If the history file does not exist, it will be created.

        Args:
            history: The history (name) to get the path of
            title: The title of new history. Only used when the history
                file does not exist.

        Returns:
            The path to the history file
        """
        history_dir = (
            Path(self.config.history_directory)
            .joinpath(self.profile)
            .expanduser()
        )
        history_dir.mkdir(parents=True, exist_ok=True)
        out = history_dir.joinpath(f"{history}.json")
        if not out.exists():
            title = json.dumps(title)
            out.write_text(f'{{"title": {title}, "history": []}}\n')
        return out

    def new_history(self, title: str | None = None) -> str:
        """Create a new history, and return its name (stem)

        Args:
            title: The title of the new history

        Returns:
            The name (stem) of the new history
        """
        hf = self.history_file(f"{time.strftime('%Y-%m-%d_%H-%M-%S')}", title)
        self.logger.info("Created new history: %s", hf.stem)
        return hf.stem

    def load_history(self, history: str) -> Mapping[str, Any]:
        """Load a history

        Args:
            history: The history (name) to load

        Returns:
            The history dict
        """
        with self.history_file(history).open() as f:
            return json.load(f)

    def rename_history(self, history: str, new_title: str) -> None:
        """Rename a history

        Args:
            history: The history (name) to rename
            new_title: The new title of the history
        """
        history_file = self.history_file(history)
        with history_file.open() as f:
            history_json = json.load(f)

        history_json["title"] = new_title

        with history_file.open("w") as f:
            json.dump(history_json, f, indent=2)

    def history_title(
        self,
        history: str,
        fallback: bool,
        add_date: bool,
    ) -> str | None:
        """Get the title of a history

        Args:
            history (str): The history (name) to get the title of
            fallback (bool): Whether to fallback to the history name
                if the title is not found or empty. Otherwise, return None.
            add_date (bool): Whether to add the date to the title
                if the title is found and not empty.

        Returns:
            str | None: The title of the history
        """
        with self.history_file(history).open() as f:
            history_json = json.load(f)

        title = history_json.get("title", None)
        if not title and not fallback:
            return None

        if not title:
            return history

        if add_date:
            title = f"{title} ({history})"

        return title

    def history_change_title(self, history: str, title: str) -> None:
        """Change the title of a history

        Args:
            history: The history (name) to change the title of
            title: The new title
        """
        with self.history_file(history).open() as f:
            history_json = json.load(f)

        history_json["title"] = title

        with self.history_file(history).open("w") as f:
            json.dump(history_json, f, indent=2)

    def history_to_prompt_history(self, history: str) -> List[str]:
        """Convert the history to a prompt-toolkit history

        Args:
            history: The history (name) to convert

        Returns:
            The prompt-toolkit history
        """
        with self.history_file(history).open() as f:
            history = json.load(f)

        if "history" not in history:
            return []

        return [
            message["data"]["content"]
            for message in history["history"]
            if message["type"] == "human"
        ]

    def query(
        self,
        query: str,
        history: str,
        callbacks: List[BaseCallbackHandler] | BaseCallbackHandler,
    ) -> Mapping[str, Any]:
        """Query the model with a string"""
        return self.ring.query(query, self.history_file(history), callbacks)

    async def a_query(
        self,
        query: str,
        history: str,
        callbacks: List[BaseCallbackHandler] | BaseCallbackHandler,
    ) -> Mapping[str, Any]:
        """Query the model with a string asynchronously"""
        return await self.ring.a_query(
            query, self.history_file(history), callbacks
        )
