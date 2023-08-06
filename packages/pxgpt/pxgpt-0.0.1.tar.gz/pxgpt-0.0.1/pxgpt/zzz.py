"""Provides a command to solve that async not supported by some chains/llms.

This command will be spawned by the server, by asyncio.create_subprocess_exec().
By communicating with the server via stdin/stdout, it can run asynchronously.
Let me know if you have a better idea.

Don't run this command manually, unless for testing purpose.
The output and logs are not optimized for human reading.
"""
from __future__ import annotations

import logging
import sys

from .logger import get_logger
from .manager import Manager
from .rings._callbacks import ZzzCallbackHandler


def from_input(prefix: str, end: str = "@on_input_end") -> str:
    """Read input from stdin with prefix

    Args:
        prefix: The prefix of the input.
        end: The end of the input.

    Returns:
        The input text.
    """
    text = ""
    while True:
        chars = input()
        if chars == end:
            break
        if not chars.startswith(f"{prefix}:"):
            continue

        text += chars[len(prefix) + 1 :] + "\n"

    return text.strip()


def zzz(profile: str):
    """The entrance of the command.

    Args:
        profile: The profile.
    """
    logger = get_logger("INFO")
    logger.removeHandler(logger.handlers[0])
    # Use sys.stdout for logging, so the parent process can read the logs.
    logger.addHandler(logging.StreamHandler(sys.stdout))
    handler = logger.handlers[0]
    # Add level names so parent process can parse
    handler.setFormatter(
        logging.Formatter("@on_log:%(levelname)s:%(message)s")
    )
    manager = Manager(profile)
    logger.warning(
        "This command is used to solve that async not supported by some LLMs. "
        "Don't run this command manually."
    )
    logger.info("You may check out the issues:")
    logger.info("https://github.com/hwchase17/langchain/issues/5210")
    logger.info("https://github.com/nomic-ai/gpt4all/issues/752")

    # Waiting for inputs.
    # If a KeyboardInterrupt is raised, the program will exit.
    while True:
        try:
            conversation = from_input("@on_conversation_input")
            logger.info("Conversation: %s", conversation)

            query = from_input("@on_query_input")
            logger.info("Query: %r", query)

            manager.query(query, conversation, ZzzCallbackHandler())

        except (EOFError, KeyboardInterrupt):
            logger.info("Exiting...")
            break
        except Exception as exc:
            logger.exception(exc)
            break
