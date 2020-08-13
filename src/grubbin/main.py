from asyncio import Queue, gather
from decimal import getcontext
from functools import partial

from asyncpg import connect, Connection

from cryptoxlib.clients.binance.BinanceClient import BinanceClient
from cryptoxlib.clients.binance.BinanceWebsocket import TradeSubscription
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair

from .postgresql import insert_binance_trade
from .binance import parse_trade

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

    postgres_connection: Connection = await connect(
        user="postgres", password="password", database="binance", host="127.0.0.1",
    )

    binance_client: BinanceClient = CryptoXLib.create_binance_client(
        binance_api_key, binance_security_key
    )

    binance_client.compose_subscriptions(
        [
            TradeSubscription(
                pair=Pair("BTC", "USDT"), callbacks=[partial(parse_trade, queue=queue)],
            )
        ]
    )

    await gather(
        binance_client.start_websockets(),
        insert_binance_trade(queue, postgres_connection),
    )

    await gather(postgres_connection.close(), binance_client.close())
