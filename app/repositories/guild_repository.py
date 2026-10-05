from __future__ import annotations

import asyncio
from typing import Any
from google.cloud.firestore_v1.client import Client

class GuildRepository:
    """Firestore access. Every guild is an isolated SaaS tenant."""

    def __init__(self, db: Client):
        self.db = db

    def _guild(self, guild_id: int):
        return self.db.collection("guilds").document(str(guild_id))

    async def ensure_guild(self, guild_id: int, name: str) -> None:
        await asyncio.to_thread(self._guild(guild_id).set, {
            "name": name,
            "active": True,
            "plan": "free",
            "prefix": "!",
            "updated_at": firestore.SERVER_TIMESTAMP,
        }, merge=True)

    async def get_settings(self, guild_id: int) -> dict[str, Any]:
        snap = await asyncio.to_thread(self._guild(guild_id).get)
        return snap.to_dict() or {}

    async def set_registration(self, guild_id: int, category_id: int, data: dict[str, Any]) -> None:
        ref = self._guild(guild_id).collection("registration_settings").document(str(category_id))
        await asyncio.to_thread(ref.set, data, merge=True)

    async def get_registration(self, guild_id: int, category_id: int) -> dict[str, Any] | None:
        ref = self._guild(guild_id).collection("registration_settings").document(str(category_id))
        snap = await asyncio.to_thread(ref.get)
        return snap.to_dict() if snap.exists else None

    async def create_tournament(self, guild_id: int, tournament_id: str, data: dict[str, Any]) -> None:
        ref = self._guild(guild_id).collection("tournaments").document(tournament_id)
        await asyncio.to_thread(ref.set, data)

    async def get_tournament(self, guild_id: int, tournament_id: str) -> dict[str, Any] | None:
        ref = self._guild(guild_id).collection("tournaments").document(tournament_id)
        snap = await asyncio.to_thread(ref.get)
        return snap.to_dict() if snap.exists else None

    async def delete_tournament(self, guild_id: int, tournament_id: str) -> None:
        ref = self._guild(guild_id).collection("tournaments").document(tournament_id)
        await asyncio.to_thread(ref.delete)

    async def create_scrim(self, guild_id: int, scrim_id: str, data: dict[str, Any]) -> None:
        ref = self._guild(guild_id).collection("scrims").document(scrim_id)
        await asyncio.to_thread(ref.set, data)

    async def get_scrim(self, guild_id: int, scrim_id: str) -> dict[str, Any] | None:
        ref = self._guild(guild_id).collection("scrims").document(scrim_id)
        snap = await asyncio.to_thread(ref.get)
        return snap.to_dict() if snap.exists else None

    async def update_scrim(self, guild_id: int, scrim_id: str, data: dict[str, Any]) -> None:
        ref = self._guild(guild_id).collection("scrims").document(scrim_id)
        await asyncio.to_thread(ref.set, data, merge=True)

    async def delete_scrim(self, guild_id: int, scrim_id: str) -> None:
        ref = self._guild(guild_id).collection("scrims").document(scrim_id)
        await asyncio.to_thread(ref.delete)

# Imported here to keep SERVER_TIMESTAMP usage centralized.
from firebase_admin import firestore
