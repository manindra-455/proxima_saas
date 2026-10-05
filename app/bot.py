from __future__ import annotations

import logging
import discord
from discord.ext import commands
from app.core.config import Settings
from app.core.firebase import initialize_firestore
from app.core.health import HealthServer
from app.repositories.guild_repository import GuildRepository

log = logging.getLogger(__name__)

class ProximaBot(commands.Bot):
    def __init__(self, settings: Settings):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.guild_messages = True
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=self.prefix_for, intents=intents, help_command=None)
        self.settings = settings
        self.repo = GuildRepository(initialize_firestore(settings))
        self.health_server = HealthServer(self, settings.port)

    async def prefix_for(self, bot, message):
        if not message.guild:
            return "!"
        settings = await self.repo.get_settings(message.guild.id)
        return commands.when_mentioned_or(settings.get("prefix", "!"))(bot, message)

    async def setup_hook(self) -> None:
        for extension in ("app.cogs.core", "app.cogs.tournaments", "app.cogs.scrims"):
            await self.load_extension(extension)
        await self.health_server.start()

    async def close(self) -> None:
        await self.health_server.stop()
        await super().close()

    async def on_ready(self) -> None:
        log.info("Logged in as %s (%s), serving %s guilds", self.user, self.user.id, len(self.guilds))

    async def on_guild_join(self, guild: discord.Guild) -> None:
        await self.repo.ensure_guild(guild.id, guild.name)
