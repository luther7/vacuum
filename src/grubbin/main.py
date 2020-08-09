from asyncio import Queue, gather
from decimal import getcontext
from functools import partial

from cryptoxlib.clients.binance.BinanceClient import BinanceClient
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair
from influxdb import InfluxDBClient

from .binance import CandlesSubscription, parse_candle
from .influxdb import write_candles

getcontext().prec = 8


async def run(
    binance_api_key: str,
    binance_security_key: str,
    influx_host: str,
    influx_port: int,
    influx_user: str,
    influx_password: str,
    influx_database: str,
    dry_run: bool = False,
) -> None:
    queue: Queue = Queue()

    influxdb_client: InfluxDBClient = InfluxDBClient(
        influx_host, influx_port, influx_user, influx_password, influx_database,
    )

    binance_client: BinanceClient = CryptoXLib.create_binance_client(
        binance_api_key, binance_security_key
    )

    binance_client.compose_subscriptions(
        [
            CandlesSubscription(
                pair=Pair("BTC", "USDT"),
                callbacks=[partial(parse_candle, queue=queue)],
            )
        ]
    )

    await gather(
        binance_client.start_websockets(), write_candles(queue, influxdb_client)
    )

    await binance_client.close()
