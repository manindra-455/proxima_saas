import logging
from app.bot import ProximaBot
from app.core.config import Settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

if __name__ == "__main__":
    settings = Settings.from_env()
    ProximaBot(settings).run(settings.discord_token, log_handler=None)
