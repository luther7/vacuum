from asyncio import Queue, Task, gather, sleep
from functools import partial
from typing import Callable, Dict, List

import attr
from cryptoxlib.clients.binance.BinanceWebsocket import (
    TradeSubscription as BinanceTradeSubscription,
)
from cryptoxlib.clients.bitforex.BitforexWebsocket import (
    TradeSubscription as BitforexTradeSubscription,
)
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair
from cryptoxlib.WebsocketMgr import Subscription

from .config import pairs
from .inserter import Inserter
from .logger import get_logger
from .models import BinanceTrade, BitforexTrade, Exchange

logger = get_logger(__name__)


async def stream() -> None:
    async with BinanceStreamer() as binance, BitforexStreamer() as bitforex:
        await gather(log_task_count(), binance.run(), bitforex.run())


async def log_task_count() -> None:
    while True:
        logger.info("tasks", extra={"count": len(Task.all_tasks())})
        await sleep(2)


@attr.s(auto_attribs=True)
class Streamer(Inserter):
    create_subscription: Callable
    parser: Callable

    subscription_args: dict = {}

    @staticmethod
    async def _parse(
        response: dict, exchange: Exchange, pair: Pair, parser: Callable, queue: Queue
    ) -> None:
        total: int = 0

        def log(message: str):
            logger.info(
                message,
                extra={
                    "exchange": exchange.name,
                    "pair": pair,
                    "response": response,
                    "total": total,
                },
            )

        log("received")

        try:
            if "data" in response:
                await parser(response, pair, queue)
        except KeyError as e:
            log("malformed response")
            raise e

    async def _aenter(self):
        await super()._aenter()  # type: ignore

        parsers: Dict[Pair, Callable] = {
            p: partial(
                Streamer._parse,
                exchange=self.exchange,
                pair=p,
                queue=self._queue,
                parser=self.parser,
            )
            for p in pairs
        }

        subscriptions: List[Subscription] = [
            self.create_subscription(pair=p, **self.subscription_args, callbacks=[c])
            for p, c in parsers.items()
        ]

        self._cryptoxlib_client.compose_subscriptions(subscriptions)

    async def _gather(self) -> None:
        await self._cryptoxlib_client.start_websockets()


async def binance_parser(response: dict, pair: Pair, queue: Queue) -> None:
    await queue.put(BinanceTrade.from_websocket_api(pair, response["data"]))


@attr.s(auto_attribs=True)
class BinanceStreamer(Streamer):
    exchange: Exchange = Exchange.binance
    create_client: Callable = CryptoXLib.create_binance_client
    create_subscription: Callable = BinanceTradeSubscription
    parser: Callable = binance_parser


async def bitforex_parser(response: dict, pair: Pair, queue: Queue) -> None:
    for t in response["data"]:
        await queue.put(BitforexTrade.from_websocket_api(pair, t))


@attr.s(auto_attribs=True)
class BitforexStreamer(Streamer):
    exchange: Exchange = Exchange.bitforex
    create_client: Callable = CryptoXLib.create_bitforex_client
    create_subscription: Callable = BitforexTradeSubscription
    parser: Callable = bitforex_parser
    subscription_args: dict = {"size": 1}
