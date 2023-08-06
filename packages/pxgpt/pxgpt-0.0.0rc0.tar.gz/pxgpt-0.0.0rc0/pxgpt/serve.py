"""Serves the web interface"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Awaitable, Callable, Coroutine

from hypercorn.config import Config as HyperConfig
from hypercorn.asyncio import serve as qserve
from quart import Quart, redirect, websocket

from .config import config
from .logger import get_logger
from .ws import WS

if TYPE_CHECKING:
    from logging import Logger


class MyQuart(Quart):
    """Subclass of Quart that uses our logger"""

    def __init__(self, *args, logger: Logger, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._logger = logger

    def run_task(
        self,
        host: str = "127.0.0.1",
        port: int = 5000,
        debug: bool | None = None,
        ca_certs: str | None = None,
        certfile: str | None = None,
        keyfile: str | None = None,
        shutdown_trigger: Callable[..., Awaitable[None]] | None = None,
    ) -> Coroutine[None, None, None]:
        """Return a task that when awaited runs this application.

        This is best used for development only, see Hypercorn for
        production servers.

        Arguments:
            host: Hostname to listen on. By default this is loopback
                only, use 0.0.0.0 to have the server listen externally.
            port: Port number to listen on.
            debug: If set enable (or disable) debug mode and debug output.
            ca_certs: Path to the SSL CA certificate file.
            certfile: Path to the SSL certificate file.
            keyfile: Path to the SSL key file.

        """
        config = HyperConfig()
        config.access_log_format = "%(h)s %(r)s %(s)s %(b)s %(D)s"
        config.accesslog = self.logger
        config.bind = [f"{host}:{port}"]
        config.ca_certs = ca_certs
        config.certfile = certfile
        if debug is not None:
            self.debug = debug
        config.errorlog = config.accesslog
        config.keyfile = keyfile

        return qserve(self, config, shutdown_trigger=shutdown_trigger)


def serve(port):
    """Serve the application with Hypercorn"""
    # Only log_level from default profile works
    logger = get_logger(config.log_level)

    app = MyQuart(
        __package__,
        static_folder=Path(__file__).parent / "frontend" / "build",
        static_url_path="/",
        logger=logger,
    )
    ws = WS()

    @app.route("/", methods=["GET"])
    def _index():
        return redirect(f"index.html")

    @app.websocket("/ws")
    async def _ws():
        """The websocket handler"""
        try:
            while True:
                message = await websocket.receive()
                message = json.loads(message)
                if message["event"] == "connect":
                    ws.ws = websocket._get_current_object()
                    await ws.on_connect(app, message)
                else:
                    fun = getattr(ws, f'on_{message["event"]}')
                    await fun(app, message)
        finally:
            await ws.on_disconnect(app)

    app.run(
        host="0.0.0.0",
        port=port,
        use_reloader=True,
    )
