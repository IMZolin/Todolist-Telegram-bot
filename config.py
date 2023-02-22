import os

from dotenv import load_dotenv

from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
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
            password=os.getenv('PG_PASSWORD'),
            username=os.getenv('DB_USER'),
            database=os.getenv('DB_NAME')
        )
    )