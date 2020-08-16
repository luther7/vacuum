from asyncio import Task, gather, sleep
from typing import Callable, Optional

import attr
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair

from .inserter import Inserter

# from .config import config, pairs
from .logger import get_logger
from .models import BinanceTrade, Exchange

logger = get_logger(__name__)


async def fetch() -> None:
    async with BinanceFetcher() as binance:
        # await gather(log_task_count(), binance.run())
        await gather(binance.run())


async def log_task_count() -> None:
    while True:
        logger.info("tasks", extra={"count": len(Task.all_tasks())})
        await sleep(2)


@attr.s(auto_attribs=True)
class Fetcher(Inserter):
    _queue_size: int = 100
    _fetch_limit: int = 1
    _amount_limit: int = 1

    async def _aenter(self, fetch_limit: int = 5, amount_limit: int = 1000):
        await super()._aenter()  # type: ignore

        self._fetch_limit = fetch_limit
        self._amount_limit = amount_limit

    async def _gather(self) -> None:
        pair: Pair = Pair("BTC", "USDT")
        from_id: Optional[int] = None
        to_id: Optional[int] = None

        for i in range(self._fetch_limit):
            logger.info(
                "fetching",
                extra={
                    "exchange": self.exchange.name,
                    "pair": pair,
                    "fetch_index": i,
                    "fetch_limit": self._fetch_limit,
                    "from_id": from_id,
                    "to_id": to_id,
                },
            )

            response: dict = await self._cryptoxlib_client.get_historical_trades(
                pair=pair, limit=self._amount_limit, from_id=from_id
            )

            try:
                body: dict = response["response"]
                from_id = body[0]["id"]
                to_id = body[-1]["id"]

                for t in response["response"]:
                    await self._queue.put(BinanceTrade.from_http_api(pair, t))

            except KeyError as e:
                logger.info(
                    "malformed response",
                    extra={
                        "exchange": self.exchange,
                        "pair": pair,
                        "response": response,
                    },
                )

                raise e

        self._complete: bool = True


@attr.s(auto_attribs=True)
class BinanceFetcher(Fetcher):
    exchange: Exchange = Exchange.binance
    create_client: Callable = CryptoXLib.create_binance_client
