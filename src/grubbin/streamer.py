from asyncio import Queue, Task, gather, sleep
from functools import partial
from typing import Callable

import attr
from asyncpg import Connection
from cryptoxlib.clients.binance.BinanceWebsocket import (
    TradeSubscription as BinanceTradeSubscription,
)
from cryptoxlib.clients.bitforex.BitforexWebsocket import (
    TradeSubscription as BitforexTradeSubscription,
)
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.CryptoXLibClient import CryptoXLibClient
from cryptoxlib.Pair import Pair

from .config import config, pairs
from .logger import get_logger
from .models import BinanceTrade, BitforexTrade, Exchange, Trade, as_postgres_row
from .postgres import get_postgres_connection

logger = get_logger(__name__)


async def stream() -> None:
    async with BinanceStreamer() as binance, BitforexStreamer() as bitforex:
        await gather(log_task_count(), binance.run(), bitforex.run())


async def log_task_count() -> None:
    while True:
        logger.info("tasks", extra={"count": len(Task.all_tasks())})
        await sleep(2)


@attr.s(auto_attribs=True)
class Streamer:
    exchange: Exchange
    create_client: Callable
    create_subscription: Callable
    parser: Callable
    subscription_args: dict = {}

    _cryptoxlib_client: CryptoXLibClient = None
    _postgres_connection: Connection = None
    _queue: Queue = attr.ib(factory=Queue)
    _complete: bool = False

    _queue_size: int = 20

    async def __aenter__(self):
        self._queue = Queue(self._queue_size)
        self._postgres_connection = await get_postgres_connection()

        self._cryptoxlib_client: CryptoXLibClient = self.create_client(
            config["exchanges"][self.exchange.name]["security_key"],
            config["exchanges"][self.exchange.name]["api_key"],
        )

        self._cryptoxlib_client.compose_subscriptions(
            [
                self.create_subscription(
                    pair=p,
                    **self.subscription_args,
                    callbacks=[partial(self.parser, pair=p, queue=self._queue)],
                )
                for p in pairs
            ]
        )

        return self

    async def __aexit__(self, *args, **kwargs):
        await self._cryptoxlib_client.close()
        await self._postgres_connection.close()

    async def _insert(self) -> None:
        while not self._complete:
            if self._queue.empty():
                await sleep(2)
                continue

            size: int = self._queue.qsize()
            logger.info(
                "inserting", extra={"exchange": self.exchange.name, "queue_size": size}
            )

            while not self._queue.empty():
                trade: Trade = await self._queue.get()
                await self._postgres_connection.copy_records_to_table(
                    f"{self.exchange.name}_trade", records=[as_postgres_row(trade)]
                )

    async def run(self) -> None:
        """
        - Open the websocket to the exchange.
        - Parse and enqueue messages from the websocket.
        - Feed the queued messaged into Postgres.
        """
        await gather(
            self._cryptoxlib_client.start_websockets(), self._insert(),
        )


async def binance_parser(response: dict, pair: Pair, queue: Queue) -> None:
    logger.info(
        "received", extra={"exchange": "binance", "pair": pair, "response": response}
    )

    try:
        await queue.put(BinanceTrade.from_websocket_api(pair, response["data"]))
    except KeyError as e:
        logger.info(
            "malformed response",
            extra={"exchange": "bitforex", "pair": pair, "response": response},
        )
        raise e


@attr.s(auto_attribs=True)
class BinanceStreamer(Streamer):
    exchange: Exchange = Exchange.binance
    create_client: Callable = CryptoXLib.create_binance_client
    create_subscription: Callable = BinanceTradeSubscription
    parser: Callable = binance_parser


async def bitforex_parser(response: dict, pair: Pair, queue: Queue) -> None:
    logger.info(
        "received", extra={"exchange": "bitforex", "pair": pair, "response": response}
    )

    try:
        if "data" in response:
            for t in response["data"]:
                await queue.put(BitforexTrade.from_websocket_api(pair, t))
    except KeyError as e:
        logger.info(
            "malformed response",
            extra={"exchange": "bitforex", "pair": pair, "response": response},
        )
        raise e


@attr.s(auto_attribs=True)
class BitforexStreamer(Streamer):
    exchange: Exchange = Exchange.bitforex
    create_client: Callable = CryptoXLib.create_bitforex_client
    create_subscription: Callable = BitforexTradeSubscription
    parser: Callable = bitforex_parser
    subscription_args: dict = {"size": 1}
