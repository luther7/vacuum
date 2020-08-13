from asyncio import Queue, sleep
from dataclasses import astuple

from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from .logger import get_logger
from .models import BinanceTrade, BitforexTrade

logger = get_logger(__name__)


async def insert_binance_trade(queue: Queue, connection: Connection) -> None:
    while True:
        logger.info(f"Queue size {queue.qsize()}", extra={"exchange": "binance"})
        if queue.empty():
            await sleep(1)

        else:
            trade: BinanceTrade = await queue.get()

            await connection.copy_records_to_table(
                "binance_trade", records=[astuple(trade)]
            )


async def insert_bitforex_trade(queue: Queue, connection: Connection) -> None:
    while True:
        logger.info(f"Queue size {queue.qsize()}", extra={"exchange": "bitforex"})

        if queue.empty():
            await sleep(1)

        else:
            trade: BitforexTrade = await queue.get()

            try:
                await connection.copy_records_to_table(
                    "bitforex_trade", records=[astuple(trade)]
                )
            except UniqueViolationError:
                pass
