from asyncio import Queue, gather, sleep
from typing import Callable

import attr
from asyncpg import Connection
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

        while True:
            if self._queue.empty():
                if self._complete:
                    logger.info(
                        "exiting",
                        extra={
                            "exchange": self.exchange.name,
                            "total": total,
                            "queue_size": self._queue_size,
                        },
                    )
                    return

                await sleep(2)
                continue

            logger.info(
                "inserting",
                extra={"exchange": self.exchange.name, "queue_size": self._queue_size},
            )

            while not self._queue.empty():
                trade: Trade = await self._queue.get()
                await self._postgres_connection.copy_records_to_table(
                    f"{self.exchange.name}_trade", records=[as_postgres_row(trade)]
                )
                total = total + 1

    async def _gather(self) -> None:
        raise NotImplementedError("Abstract method")
