from asyncio import Queue, sleep
from dataclasses import astuple

from asyncpg import Connection, connect

from .models import Candle


async def write_candles(queue: Queue) -> None:
    while True:
        if queue.empty():
            print("Wait to write candle")
            await sleep(1)

        else:
            print("Writing candle")

            connection: Connection = await connect(
                user="postgres",
                password="password",
                database="binance",
                host="127.0.0.1",
            )

            candle: Candle = await queue.get()

            print(_candle_record(candle))
            await connection.copy_records_to_table(
                "candles", records=[_candle_record(candle)]
            )

            await connection.close()


def _candle_record(candle: Candle) -> tuple:
    return astuple(candle)
