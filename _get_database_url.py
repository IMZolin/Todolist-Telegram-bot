from data.config import load_config


DATABASE_URI = f'sqlite:///data/database.sqlite3'
config = load_config()

if config.db.username and config.db.password and config.db.host and config.db.port and config.db.database:
    DATABASE_URI = f'postgresql://{config.db.username}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}'

print(DATABASE_URI)