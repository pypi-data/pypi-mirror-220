"""Provides the CLI chat interface"""
from __future__ import annotations

import asyncio
import time
from typing import List, Tuple

from prompt_toolkit.shortcuts import PromptSession, set_title
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from .version import __version__
from .manager import Manager

from .rings._callbacks import DocumentStreamingStdOutCallbackHandler


CHAT_COMMANDS = {
    "/help": "List the commands",
    "/new": "Start a new conversation",
    "/switch": "Switch to a conversation",
    "/list": "List all conversations",
    "/path": "Show the path of the current conversation file",
    "/delete": "Delete a conversation",
    "/rename": "Rename a conversation",
    "/ingest": "Ingest documents from the source directory",
    "/docs": "List ingested and uningested documents in the source directory",
    "/exit": "Exit the CLI",
}

CHAT_COMMAND_HELPS = {
    "/help": [
        "/help: List all commands",
        "/help [command]: Show the help for a command",
        "/help [/command]: Show the help for a command",
    ],
    "/new": [
        "/new: Start a new conversation",
        "/new [title]: Start a new conversation with a title",
    ],
    "/switch": [
        "/switch [datetime]: Switch to a conversation named like 2021-01-01_00-00-00",
        "/switch [index]: Switch to a conversation by index (use /list to see the index)",
    ],
    "/delete": [
        "/delete: Delete current conversation",
        "/delete [datetime]: Delete a conversation named like 2021-01-01_00-00-00",
        "/delete [index]: Delete a conversation by index (use /list to see the index)",
    ],
    "/rename": [
        "/rename <title>: Rename current conversation to <title>",
    ],
    "/ingest": [
        "/ingest: Ingest documents from the source directory",
        "/ingest force: Force ingestion, even if the document exists",
        "/ingest f: Force ingestion, even if the document exists",
        "/ingest --force: Force ingestion, even if the document exists",
        "/ingest -f: Force ingestion, even if the document exists",
    ],
}


class ChatCommand:
    """Manage the chat commands"""

    def __init__(
        self,
        manager: Manager,
        session: PromptSession,
        history: str,
        history_list: List[str],
    ):
        self.manager = manager
        self.session = session
        self.history = history
        self.history_list = history_list

    @classmethod
    def get_command_and_args(cls, query: str) -> Tuple[str, List[str]] | bool:
        """Get the command and the arguments from a query

        Args:
            query: The query string

        Returns:
            False if query does not start with "/"
            (command, args) if query starts with "/"
            When command is not a known command, returns (command, False)
        """
        if not query.startswith("/"):
            # not a command, continue query
            return False

        cmd, *args = query.split(" ")
        if cmd not in CHAT_COMMANDS:
            # is a command, but not a known one, don't continue query
            return cmd, False

        return cmd, args

    async def a_run(self, cmd: str, args: List[str]) -> bool | None:
        """Run a command asynchronously

        Args:
            cmd: The command
            args: The arguments

        Returns:
            False to break the loop
        """
        method = f"_{cmd[1:]}"
        amethod = f"_a_{cmd[1:]}"

        if hasattr(self, amethod):
            fun = getattr(self, amethod)
            return await fun(args)

        if hasattr(self, method):
            fun = getattr(self, method)
            return fun(args)

        print(f"Error: Unknown command: {cmd}")
        return False

    def run(self, cmd: str, args: List[str]) -> bool | None:
        """Run a command

        Args:
            cmd: The command
            args: The arguments

        Returns:
            False to break the loop
        """
        method = f"_{cmd[1:]}"

        if hasattr(self, method):
            fun = getattr(self, method)
            return fun(args)

        print(f"Error: Unknown command: {cmd}")
        return False

    def _help(self, args: List[str]) -> None:
        """Show the help for a command"""
        if not args:
            print("Commands:")
            for cmd, desc in CHAT_COMMANDS.items():
                print(f"  - {cmd}: {desc}")
        elif len(args) > 1:
            print("Error: Too many arguments")
        else:
            cmd = args[0]
            if not cmd.startswith("/"):
                cmd = "/" + cmd
            if cmd not in CHAT_COMMANDS:
                print(f"Error: Unknown command: {cmd}")
                return
            print(f"Command: {cmd}")
            help = CHAT_COMMAND_HELPS.get(cmd, f"{cmd}: {CHAT_COMMANDS[cmd]}")
            if isinstance(help, str):
                print(f"  - {help}")
            else:
                for h in help:
                    print(f"  - {h}")

    def _list(self, args: List[str]) -> None:
        """List all conversations"""
        print("Conversations:")
        for i, history in enumerate(self.history_list):
            bullet = "*" if history == self.history else "-"
            title = self.manager.history_title(
                history,
                fallback=True,
                add_date=True,
            )
            print(f"  {bullet} {i + 1}. {title}")

    def _new_(self, args: List[str], asyn: bool) -> None:
        """Start a new conversation"""
        title = " ".join(args) if args else None
        history = self.manager.new_history(title)
        self.history_list.insert(0, history)
        # recycle previous session
        del self.session
        _run_history(history, "Created a new conversation: ", self.manager, self.history_list, asyn)

    def _new(self, args: List[str]) -> None:
        """Start a new conversation"""
        self._new_(args, False)
        # exit previous session loop
        return False

    async def _a_new(self, args: List[str]) -> None:
        """Start a new conversation asynchronously"""
        self._new_(args, True)
        return False

    def _switch_(self, args: List[str], asyn: bool) -> None:
        """Switch to a conversation"""
        if not args:
            print("Error: Missing argument")
            return
        if len(args) > 1:
            print("Error: Too many arguments")
            return
        arg = args[0]
        if arg.isdigit():
            try:
                history = self.history_list[int(arg) - 1]
            except IndexError:
                print(f"Error: Invalid index: {arg}")
                return
        else:
            history = arg
            if history not in self.history_list:
                print(f"Error: Unknown conversation: {history}")
                return
        # recycle previous session
        del self.session
        _run_history(history, "Switched to conversation: ", self.manager, self.history_list, asyn)

    def _switch(self, args: List[str]) -> None:
        """Switch to a conversation"""
        self._switch_(args, False)
        # exit previous session loop
        return False

    async def _a_switch(self, args: List[str]) -> None:
        """Switch to a conversation asynchronously"""
        self._switch_(args, True)
        return False

    def _delete_(self, args: List[str], asyn: bool) -> None:
        """Delete a conversation"""
        if len(args) > 1:
            print("Error: Too many arguments")
            return

        arg = args[0]
        if arg.isdigit():
            try:
                history = self.history_list[int(arg) - 1]
            except IndexError:
                print(f"Error: Invalid index: {arg}")
                return
        else:
            history = arg
            if history not in self.history_list:
                print(f"Error: Unknown conversation: {history}")
                return

        self.manager.history_file(history).unlink()
        self.history_list.remove(history)
        print(f"Deleted conversation: {history}")

        if history == self.history:
            if self.history_list:
                del self.session
                # recycle previous session
                _run_history(self.history_list[0], "Switched to conversation: ", self.manager, self.history_list, asyn)
            else:
                self._new_([], asyn)

            return False

    def _delete(self, args: List[str]) -> None:
        """Delete a conversation"""
        return self._delete_(args, False)

    async def _a_delete(self, args: List[str]) -> None:
        """Delete a conversation asynchronously"""
        return self._delete_(args, True)

    def _path(self, args: List[str]) -> None:
        """Show the path of the current conversation file"""
        print("Path of the current conversation file:")
        print(" ", self.manager.history_file(self.history))

    def _rename(self, args: List[str]) -> None:
        """Rename a conversation"""
        if not args:
            print("Error: Missing argument")
            return

        title = " ".join(args)
        self.manager.history_change_title(self.history, title=title)
        print(f"Renamed conversation to: {title}")

    def _ingest(self, args: List[str]) -> None:
        """Ingest documents from the source directory"""
        if self.manager.config.ingest.source_directory is None:
            print("Error: No source directory set in the config")
            return

        force = args and args[0] in ("force", "f", "--force", "-f")
        self.manager.ingest(force=force)

    def _docs(self, args: List[str]) -> None:
        """List ingested and uningested documents in the source directory"""
        if self.manager.config.ingest.source_directory is None:
            print("Error: No source directory set in the config")
            return

        docs = self.manager.get_docs()
        print("Ingested documents:")
        if docs["ingested"]:
            for doc in docs["ingested"]:
                print(f"  - {doc['name']}")
        else:
            print("  - None")
        print()

        print("Documents pending ingestion:")
        if docs["pending"]:
            for doc in docs["pending"]:
                print(f"  - {doc['name']}")

            # print("  You can ingest them with /ingest")
        else:
            print("  - None")

    def _exit(self, args: List[str]) -> None:
        """Exit the CLI"""
        raise EOFError()


async def _a_chat(
    manager: Manager,
    session: PromptSession,
    history: str,
    history_list: List[str],
) -> None:
    """Run the chat asynchronously"""
    last_query_took = 0
    chat_command = ChatCommand(manager, session, history, history_list)
    while True:
        try:
            if last_query_took > 0.0:
                query = await session.prompt_async(
                    bottom_toolbar=f"Last query took {last_query_took} s."
                )
            else:
                query = await session.prompt_async()

            query = query.strip()
            cmd_args = ChatCommand.get_command_and_args(query)
            if cmd_args is not False:
                cmd, args = cmd_args
                if args is False:
                    print(f"Error: Unknown command: {cmd}")
                    continue

                if await chat_command.a_run(cmd, args) is False:
                    break
                else:
                    continue

            start = time.perf_counter()
            await manager.a_query(
                query,
                history,
                callbacks=[DocumentStreamingStdOutCallbackHandler()],
            )

            last_query_took = round(time.perf_counter() - start, 2)
            print()

        except (EOFError, KeyboardInterrupt):
            print("Bye!")
            return


def _chat(
    manager: Manager,
    session: PromptSession,
    history: str,
    history_list: List[str],
) -> None:
    """Run the chat"""
    last_query_took = 0
    chat_command = ChatCommand(manager, session, history, history_list)
    while True:
        try:
            if last_query_took > 0.0:
                query = session.prompt(
                    bottom_toolbar=f"Last query took {last_query_took} s."
                )
            else:
                query = session.prompt()

            query = query.strip()
            if not query:
                continue

            cmd_args = ChatCommand.get_command_and_args(query)
            if cmd_args is not False:
                cmd, args = cmd_args
                if args is False:
                    print(f"Error: Unknown command: {cmd}")
                    continue

                if chat_command.run(cmd, args) is False:
                    break
                else:
                    continue

            start = time.perf_counter()
            manager.query(
                query,
                history,
                callbacks=[DocumentStreamingStdOutCallbackHandler()],
            )

            last_query_took = round(time.perf_counter() - start, 2)
            print()

        except (EOFError, KeyboardInterrupt):
            print("Bye!")
            return


def _run_history(
    history_name: str,
    msg: str,
    manager: Manager,
    history_list: List[str],
    asyn: bool,
) -> None:
    """Run the history/conversation"""

    history_title = manager.history_title(
        history_name,
        fallback=True,
        add_date=True,
    )
    print(msg, history_title)

    history = manager.history_to_prompt_history(history_name)

    print("Use the up/down arrow keys to navigate history.")
    print("Use /help to see the list of commands.")

    session = PromptSession(
        "\n>>> ",
        history=InMemoryHistory(history),
        auto_suggest=AutoSuggestFromHistory(),
    )
    set_title("pxGPT CLI")

    if asyn:
        asyncio.run(_a_chat(manager, session, history_name, history_list))
    else:
        _chat(manager, session, history_name, history_list)


def chat_cli(profile: str, asyn: bool) -> None:
    """Chat with the model in the terminal"""
    print()
    print(f"Welcome to chat via the pxGPT CLI v{__version__}!")
    print("Hit 'Ctrl+c' or 'Ctrl+d' to exit.")

    manager = Manager(profile)
    history = None
    history_list = manager.get_histories()

    if not history_list:
        history_list = [manager.new_history()]
        msg = "Created a new conversation: "
    else:
        msg = "Loaded conversation: "

    history = history_list[0]
    _run_history(history, msg, manager, history_list, asyn)
