# Proxima SaaS Discord Bot

A multi-tenant Discord bot foundation using Firestore. Each Discord guild is a tenant under `guilds/{guild_id}`.

## Firestore layout

```text
guilds/{guild_id}
  plan, active, prefix, name
  tournaments/{tournament_id}
  registration_settings/{category_id}
  scrims/{scrim_id}
```

This removes local JSON files, which are unsafe on Render's ephemeral filesystem and unsafe with multiple bot instances.

## Local setup

1. Use Python 3.12 and install: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env`.
3. Set `DISCORD_TOKEN` and one Firebase credential option.
4. In Discord Developer Portal enable **Message Content Intent** and **Server Members Intent**.
5. Run: `python -m app.main`
6. Check `http://localhost:10000/health`.

## Render

Create a Blueprint from `render.yaml`, then add secret environment variables. `FIREBASE_CREDENTIALS_JSON` should contain the full service-account JSON. Do not commit the key file. Render checks `/health`.

> Use a paid always-on web service for a persistent Discord connection. Free services may sleep.

## SaaS notes

- Guild ID is the tenant boundary on every repository operation.
- Add billing fields (`plan`, `subscription_status`, limits) to each guild document.
- Enforce plan limits in a service layer before creating tournaments/scrims.
- Only run one bot instance until scheduled jobs use distributed locking.
- Firestore calls are wrapped with `asyncio.to_thread` because Firebase Admin's Python client is synchronous.

## What changed from the supplied monolith

- One `on_message`/`on_ready` lifecycle instead of duplicate event handlers.
- Firestore replaces all JSON reads/writes.
- Discord objects are stored as IDs, never serialized objects.
- `/health` binds to `0.0.0.0:$PORT` for Render.
- Commands are split into cogs and all records are scoped by guild.
- Fixed command names and ID type mismatches.

The scaffold implements the command lifecycle and storage layer. Port specialized interactive modal flows from the old file into `views/`; they should call `bot.repo` rather than global dictionaries.
