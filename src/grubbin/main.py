from asyncio import Queue, gather
from functools import partial

from asyncpg import Connection, connect
from cryptoxlib.clients.binance.BinanceClient import BinanceClient
from cryptoxlib.clients.bitforex.BitforexClient import BitforexClient
from cryptoxlib.clients.binance.BinanceWebsocket import (
    TradeSubscription as BinanceTradeSubscription,
)
from cryptoxlib.clients.bitforex.BitforexWebsocket import (
    TradeSubscription as BitforexTradeSubscription,
)
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair

from .apis import parse_binance_trade, parse_bitforex_trade
from .postgresql import insert_binance_trade, insert_bitforex_trade


async def run(
    binance_api_key: str,
    binance_security_key: str,
    bitforex_api_key: str,
    bitforex_security_key: str,
    postgres_host: str,
    postgres_port: int,
    postgres_user: str,
    postgres_password: str,
    postgres_database: str,
    dry_run: bool = False,
) -> None:

    binance_postgres_connection: Connection = await connect(
        host=postgres_host,
        port=postgres_port,
        user=postgres_user,
        password=postgres_password,
        database=postgres_database,
    )

    bitforex_postgres_connection: Connection = await connect(
        host=postgres_host,
        port=postgres_port,
        user=postgres_user,
        password=postgres_password,
        database=postgres_database,
    )

    binance_queue: Queue = Queue()
    bitforex_queue: Queue = Queue()

    binance_client: BinanceClient = CryptoXLib.create_binance_client(
        binance_api_key, binance_security_key
    )

    binance_client.compose_subscriptions(
        [
            BinanceTradeSubscription(
                pair=Pair("BTC", "USDT"),
                callbacks=[partial(parse_binance_trade, queue=binance_queue)],
            )
        ]
    )

    bitforex_client: BitforexClient = CryptoXLib.create_bitforex_client(
        bitforex_api_key, bitforex_security_key
    )

    bitforex_client.compose_subscriptions(
        [
            BitforexTradeSubscription(
                pair=Pair("BTC", "USDT"),
                size=1,
                callbacks=[partial(parse_bitforex_trade, queue=bitforex_queue)],
            )
        ]
    )

    await gather(
        binance_client.start_websockets(),
        bitforex_client.start_websockets(),
        insert_binance_trade(binance_queue, binance_postgres_connection),
        insert_bitforex_trade(bitforex_queue, bitforex_postgres_connection),
    )

    await gather(
        binance_postgres_connection.close(),
        bitforex_postgres_connection.close(),
        bitforex_client.close(),
        binance_client.close(),
    )
