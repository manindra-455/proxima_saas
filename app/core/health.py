from __future__ import annotations

from aiohttp import web

class HealthServer:
    def __init__(self, bot, port: int):
        self.bot = bot
        self.port = port
        self.runner: web.AppRunner | None = None

    async def health(self, request: web.Request) -> web.Response:
        ready = self.bot.is_ready()
        return web.json_response({
            "status": "ok" if ready else "starting",
            "discord_ready": ready,
            "guilds": len(self.bot.guilds),
        }, status=200)  # Keep 200 during Discord reconnects so Render does not restart-loop.

    async def root(self, request: web.Request) -> web.Response:
        return web.json_response({"service": "proxima-bot", "health": "/health"})

    async def start(self) -> None:
        app = web.Application()
        app.router.add_get("/", self.root)
        app.router.add_get("/health", self.health)
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        await web.TCPSite(self.runner, "0.0.0.0", self.port).start()

    async def stop(self) -> None:
        if self.runner:
            await self.runner.cleanup()
