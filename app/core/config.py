from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True, slots=True)
class Settings:
    discord_token: str
    firebase_credentials_json: str | None
    firebase_credentials_path: str | None
    firebase_project_id: str | None
    port: int
    environment: str

    @classmethod
    def from_env(cls) -> "Settings":
        token = os.getenv("DISCORD_TOKEN") or os.getenv("DIS_TOKEN")
        if not token:
            raise RuntimeError("DISCORD_TOKEN is required")
        return cls(
            discord_token=token,
            firebase_credentials_json=os.getenv("FIREBASE_CREDENTIALS_JSON"),
            firebase_credentials_path=os.getenv("FIREBASE_CREDENTIALS_PATH"),
            firebase_project_id=os.getenv("FIREBASE_PROJECT_ID"),
            port=int(os.getenv("PORT", "10000")),
            environment=os.getenv("ENVIRONMENT", "development"),
        )
