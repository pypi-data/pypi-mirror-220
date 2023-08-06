from __future__ import annotations
import asyncio
import sys

from typing import Any, Mapping
from quart import Quart

import yaml
from simpleconf import ProfileConfig
from simpleconf.utils import POOL_KEY

from .logger import get_logger
from .config import (
    CONFIG_SCHEMA,
    MY_CONFIG_FILE,
    config,
)
from .rings._callbacks import StreamingWebsocketCallbackHandler
from .manager import Manager


class WS:

    def __init__(self) -> None:
        self.config = config
        self.logger = get_logger(config.log_level)
        self.ws = None
        # Each ws connection should have one profile
        self._profile = "default"
        self.manager = None

    @property
    def profile(self) -> str:
        return self._profile

    @profile.setter
    def profile(self, value: str) -> None:
        if value == self.profile:
            return
        self._profile = value
        ProfileConfig.use_profile(self.config, self.profile)

    async def on_connect(
        self,
        app: Quart,
        data: Mapping[str, Any],
    ) -> None:
        """Run on websocket connect"""
        self.logger.info("Websocket connected from client")
        # determine profile, from the web.
        await self.ws.send_json({"event": "get_saved_profile"})

    async def on_saved_profile_obtained(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Run on websocket saved profile obtained"""
        self.profile = data["profile"]
        # profile determined, init the manager
        self.manager = Manager(self.profile, serving=True)

        await self.ws.send_json(
            {
                "event": "initialized",
                "histories": self.manager.get_histories(True),
                "profiles": ProfileConfig.profiles(self.config),
                "ingestable": bool(self.config.ingest.source_directory),
            }
        )

    async def on_disconnect(self, app: Quart) -> None:
        """Run on websocket disconnect"""
        self.logger.info("Websocket disconnected from client")
        self.ws = None

    async def on_query(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Run on websocket query"""
        if not self.manager:
            await self.ws.send_json(
                {
                    "event": "lc_error",
                    "error": "Manager not initialized",
                    "type": "custom",
                }
            )

        query, conversation = (
            data["query"],
            data.get("conversation", None),
        )
        if not conversation:
            title = query.splitlines()[0]
            conversation = self.manager.new_history(title=title)
            await self.ws.send_json(
                {
                    "event": "query_started",
                    "conversation": conversation,
                    "title": title,
                }
            )

        async def query_in_background() -> None:
            """Run query in background"""
            try:
                await self.manager.a_query(
                    query,
                    conversation,
                    StreamingWebsocketCallbackHandler(self.ws),
                )
            except Exception as ex:
                self.logger.exception(str(ex))
                await self.ws.send_json(
                    {
                        "event": "lc_error",
                        "error": str(ex),
                        "type": "custom",
                    }
                )

        app.add_background_task(query_in_background)

    async def on_load_conversation(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Run on websocket load conversation"""
        conversation = data["conversation"]
        messages = self.manager.load_history(conversation).get("history", [])
        await self.ws.send_json(
            {
                "event": "conversation_loaded",
                "messages": [
                    {
                        "when": "Earlier",
                        "who": message["type"],
                        "message": message["data"]["content"],
                    }
                    for message in messages
                ],
            }
        )

    async def on_delete_conversation(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Run on websocket delete conversation"""
        conversation = data["conversation"]
        try:
            self.manager.history_file(conversation).unlink()
        except Exception as ex:
            await self.ws.send_json(
                {
                    "event": "conversation_deleted",
                    "ok": False,
                    "error": str(ex),
                    "isCurrent": data["isCurrent"],
                    "title": data["title"],
                }
            )
        else:
            await self.ws.send_json(
                {
                    "event": "conversation_deleted",
                    "ok": True,
                    "conversation": conversation,
                    "isCurrent": data["isCurrent"],
                    "title": data["title"],
                }
            )

    async def on_rename_conversation(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Run on websocket rename conversation"""
        self.logger.info("Renaming conversation: %s", data["conversation"])
        conversation, new_title = data["conversation"], data["new_title"]
        try:
            self.manager.rename_history(conversation, new_title)
        except Exception as ex:
            await self.ws.send_json(
                {
                    "event": "conversation_renamed",
                    "ok": False,
                    "error": str(ex),
                }
            )
        else:
            await self.ws.send_json(
                {
                    "event": "conversation_renamed",
                    "ok": True,
                    "title": new_title,
                    "name": conversation,
                }
            )

    async def on_get_config(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Get profiles and configs"""
        configs = self.config[POOL_KEY]
        profile = data["profile"]

        config = configs[profile]
        default = configs["default"]
        config_schema = {}

        for key, value in CONFIG_SCHEMA.items():
            config_schema[key] = value.copy()
            # Until we support editing the config in the web interface
            config_schema[key]["readonly"] = True
            if "." in key:
                parent, child = key.split(".", 1)
                try:
                    config_schema[key]["value"] = config[parent][child]
                except KeyError:
                    pass
                config_schema[key]["default"] = default[parent][child]
            elif key in config:
                config_schema[key]["value"] = config[key]
                config_schema[key]["default"] = default[key]
            else:
                config_schema[key]["default"] = default[key]

        await self.ws.send_json(
            {
                "event": "config_obtained",
                "configSchema": config_schema,
            }
        )

    # async def on_save_config(self, app: Quart, data: Mapping[str, Any]) -> None:
    #     """Run on websocket save config"""
    #     profile, config_schema = data["profile"], data["configSchema"]
    #     configs = load_toml(MY_CONFIG_FILE)
    #     # New profile
    #     if profile not in configs:
    #         configs[profile] = {}
    #     config = configs[profile]
    #     for key, value in config_schema.items():
    #         if "value" in value:
    #             config[key] = value["value"]

    #     try:
    #         save_toml(MY_CONFIG_FILE, configs)
    #         if profile not in self.config[POOL_KEY]:
    #             self.config[POOL_KEY][profile] = {}
    #         self.config[POOL_KEY][profile].update(config)
    #     except Exception as ex:
    #         await self.ws.send_json(
    #             {
    #                 "event": "config_saved",
    #                 "ok": False,
    #                 "error": str(ex),
    #             }
    #         )
    #     else:
    #         if (profile, "web") in Manager.MANAGERS:
    #             # delete the cache, as the config has changed
    #             # we need to re-init the model
    #             del Manager.MANAGERS[(profile, "web")]

    #         await self.ws.send_json(
    #             {
    #                 "event": "config_saved",
    #                 "ok": True,
    #                 "willLoad": data.get("willLoad", False),
    #                 "profile": profile,
    #             }
    #         )
    #         restart()

    async def on_load_profile(self, app: Quart, data: Mapping[str, Any]) -> None:
        if self.manager:
            self.manager.close()
            self.manager = None

    async def on_delete_profile(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Run on websocket delete profile"""
        profile = data["profile"]
        with open(MY_CONFIG_FILE) as f:
            configs = yaml.load(f)
        try:
            del configs[profile]
            with open(MY_CONFIG_FILE, "w") as f:
                yaml.dump(configs, f)
            del self.config[POOL_KEY][profile]
        except Exception as ex:
            await self.ws.send_json(
                {
                    "event": "profile_deleted",
                    "ok": False,
                    "error": str(ex),
                }
            )
        else:
            await self.ws.send_json(
                {
                    "event": "profile_deleted",
                    "ok": True,
                }
            )

    async def on_get_docs(self, app: Quart, data: Mapping[str, Any]) -> None:
        """Run on websocket get ingested"""
        p = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "pxgpt",
            "docs",
            "-p",
            data["profile"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await p.communicate()
        if p.returncode != 0:
            await self.ws.send_json(
                {
                    "event": "docs_failed",
                    "error": stderr.decode(),
                }
            )
        else:
            # parse the stdout
            # It's like
            # Ingested documents:
            # - scGAN.pdf: /path/to/scGAN.pdf
            # Pending documents:
            # - AttentionIsAllYouNeed.pdf: /path/to/AttentionIsAllYouNeed.pdf
            stdout = stdout.decode()
            docs = {"ingested": None, "pending": None}
            for line in stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line == "Ingested documents:":
                    docs["ingested"] = []
                elif line == "Pending documents:":
                    docs["pending"] = []
                elif line.startswith("- "):
                    name, path = line[2:].split(": ", 1)
                    if isinstance(docs["pending"], list):
                        docs["pending"].append({"name": name, "path": path})
                    elif isinstance(docs["ingested"], list):
                        docs["ingested"].append({"name": name, "path": path})

            await self.ws.send_json(
                {
                    "event": "docs_obtained",
                    "docs": docs,
                }
            )
