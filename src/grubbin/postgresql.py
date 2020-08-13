from asyncio import Queue, sleep
from dataclasses import astuple

from asyncpg import Connection

from .logger import get_logger
from .models import BinanceTrade

logger = get_logger(__name__)


async def insert_binance_trade(queue: Queue, connection: Connection) -> None:
    while True:
        if queue.empty():
            logger.info("Wait to write Binance Trade")
            await sleep(1)

        else:
            logger.info("Writing Binance Trade")
            logger.info(f"Queue size {queue.qsize()}")

            trade: BinanceTrade = await queue.get()

            await connection.copy_records_to_table(
                "binance_trade", records=[astuple(trade)]
            )
