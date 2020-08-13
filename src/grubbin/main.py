from asyncio import Queue, gather
from functools import partial
from asyncpg import connect, Connection
from cryptoxlib.clients.binance.BinanceClient import BinanceClient
from cryptoxlib.clients.binance.BinanceWebsocket import TradeSubscription
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair
from .postgresql import insert_binance_trade
from .binance import parse_trade


async def run(
    binance_api_key: str,
    binance_security_key: str,
    postgres_host: str,
    postgres_port: int,
    postgres_user: str,
    postgres_password: str,
    postgres_database: str,
    dry_run: bool = False,
) -> None:
    queue: Queue = Queue()

    postgres_connection: Connection = await connect(
        host=postgres_host,
        port=postgres_port,
        user=postgres_user,
        password=postgres_password,
        database=postgres_database,
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
