from asyncio import Queue, gather, sleep
from typing import Callable

import attr
from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError
from cryptoxlib.CryptoXLibClient import CryptoXLibClient

from .config import config
from .logger import get_logger
from .models import Exchange, Trade, as_postgres_row
from .postgres import get_postgres_connection

logger = get_logger(__name__)


class Inserter:
    exchange: Exchange
    create_client: Callable

    _cryptoxlib_client: CryptoXLibClient = None
    _postgres_connection: Connection = None
    _queue: Queue = attr.ib(factory=Queue)
    _queue_size: int = 20
    _complete = False

    async def __aenter__(self, *args, **kwargs):
        await self._aenter(*args, **kwargs)  # type: ignore
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._cryptoxlib_client.close()
        await self._postgres_connection.close()

    async def _aenter(self):
        self._queue = Queue(self._queue_size)
        self._postgres_connection = await get_postgres_connection()
        self._cryptoxlib_client: CryptoXLibClient = self.create_client(
            api_key=config["exchanges"][self.exchange.name]["api_key"],
            sec_key=config["exchanges"][self.exchange.name]["security_key"],
        )

    async def run(self) -> None:
        await gather(
            self._gather(), self._insert(),
        )

    async def _insert(self) -> None:
        total: int = 0
        duplicates: int = 0

        while True:

            def log(message: str):
                logger.info(
                    message,
                    extra={
                        "exchange": self.exchange.name,
                        "total": total,
                        "duplicates": duplicates,
                        "queue_size": self._queue_size,
                    },
                )

            if self._queue.empty():
                if self._complete:
                    log("finished inserting")
                    return

                await sleep(2)
                continue

            log("inserting")
            while not self._queue.empty():
                trade: Trade = await self._queue.get()

                try:
                    await self._postgres_connection.copy_records_to_table(
                        f"{self.exchange.name}_trade", records=[as_postgres_row(trade)]
                    )

                except UniqueViolationError:
                    duplicates += 1

                total += 1

    async def _gather(self) -> None:
        raise NotImplementedError("Abstract method")
