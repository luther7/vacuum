from asyncio import Queue, sleep
from dataclasses import asdict
from typing import List

from influxdb import InfluxDBClient

from .models import Candle


async def write_candles(queue: Queue, influxdb_client: InfluxDBClient) -> None:
    while True:
        if queue.empty():
            print("Wait to write candle")
            await sleep(1)

        else:
            print("Writing candle")
            candle: Candle = await queue.get()
            influxdb_client.write_points(_candle_points(candle))


def _candle_points(candle: Candle) -> List[dict]:
    def _point(candle: Candle, time: str) -> dict:
        return {
            "measurement": candle.stream,
            "tags": {"stream": candle.stream},
            "time": time,
            "fields": asdict(candle),
        }

    return [
        _point(candle, candle.kline_start_timestamp),
        _point(candle, candle.kline_close_timestamp),
    ]
