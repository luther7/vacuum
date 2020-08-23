from asyncio import sleep

from asyncpg import Connection, connect

from .config import config
from .state import state

POSTGRES_HEALTHCHECK_TASK_NAME: str = "postgres_healthcheck"


async def get_postgres_connection() -> Connection:
    return await connect(
        host=config["postgres"]["host"],
        port=config["postgres"]["port"],
        user=config["postgres"]["user"],
        password=config["postgres"]["password"],
        database=config["postgres"]["database"],
    )


async def postgres_healthcheck() -> Connection:
    while True:
        try:
            await get_postgres_connection()
            state.postgres = True

        except Exception as exception:
            state.postgres = False
            state.postgres_error = str(exception)

        await sleep(config["postgres"]["health_check_interval"])
