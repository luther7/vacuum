from asyncio import Queue, sleep
from dataclasses import astuple

from asyncpg import Connection

from .models import BinanceTrade


async def insert_binance_trade(queue: Queue, connection: Connection) -> None:
    while True:
        if queue.empty():
            print("Wait to write Binance Trade")
            await sleep(1)

        else:
            print("Writing Binance Trade")
            print(f"Queue size {queue.qsize()}")

            trade: BinanceTrade = await queue.get()

            await connection.copy_records_to_table(
                "binance_trade", records=[astuple(trade)]
            )
