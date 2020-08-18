from asyncpg import Connection, connect

from .config import config


async def get_postgres_connection() -> Connection:
    return await connect(
        host=config["postgres"]["host"],
        port=config["postgres"]["port"],
        user=config["postgres"]["user"],
        password=config["postgres"]["password"],
        database=config["postgres"]["database"],
    )
