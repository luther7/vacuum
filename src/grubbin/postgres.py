from asyncpg import Connection, connect

from .config import config


async def get_postgres_connection() -> Connection:
    return await connect(
        host=config["postgres_host"],
        port=config["postgres_port"],
        user=config["postgres_user"],
        password=config["postgres_password"],
        database=config["postgres_database"],
    )
