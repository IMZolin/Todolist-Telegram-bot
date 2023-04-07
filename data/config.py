import os

from dotenv import load_dotenv

from dataclasses import dataclass
from pathlib import Path

DIR = Path(__file__).absolute().parent
I18N_DOMAIN = 'bot'
LOCALES_DIR = f'{DIR}/locales'
ADMINS = [int(_) for _ in os.getenv('ADMINS', default='').split()]
RATE_LIMIT = os.getenv('RATE_LIMIT')


@dataclass
class WebhookConfig:
    host: str
    port: str
    path: str


@dataclass
class DatabaseConfig:
    host: str
    port: str
    password: str
    username: str
    database: str


@dataclass
class BotConfig:
    token: str
    admins: tuple[int]
    use_redis: bool
    redis_password: str = None


@dataclass
class Config:
    bot: BotConfig
    db: DatabaseConfig


def load_config():
    load_dotenv()

    return Config(bot=BotConfig(
        token=os.getenv('BOT_TOKEN'),
        admins=(12345,),
        use_redis=True,
        redis_password=os.getenv('REDIS_PASSWORD')),
        db=DatabaseConfig(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            password=os.getenv('DB_PASSWORD'),
            username=os.getenv('DB_USER'),
            database=os.getenv('DB_NAME')
        )
    )

config = load_config().bot