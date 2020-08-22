from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Optional

import attr
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair

from .inserter import Inserter

# from .config import config, pairs
from .logger import get_logger
from .models import BinanceTrade, Exchange
from .utilities import epoch_ms_to_datetime

logger = get_logger(__name__)


async def fetch() -> None:
    async with BinanceFetcher() as binance:
        await binance.run()


@dataclass
class Window:
    from_id: Optional[int] = None
    to_id: Optional[int] = None
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None
    next_id: Optional[int] = None

    @classmethod
    def from_response(cls, response: dict, amount_limit: int) -> "Window":
        return cls(
            from_id=response[0]["id"],
            to_id=response[-1]["id"],
            from_time=epoch_ms_to_datetime(response[0]["time"]),
            to_time=epoch_ms_to_datetime(response[-1]["time"]),
            next_id=response[0]["id"] - amount_limit,
        )


@attr.s(auto_attribs=True)
class Fetcher(Inserter):
    _queue_size: int = 100
    # FIXME
    _fetch_limit: int = 1
    _amount_limit: int = 1
    _pair: Pair = None

    async def _aenter(
        self,
        pair: Pair = Pair("BTC", "USDT"),
        fetch_limit: int = 5,
        amount_limit: int = 1000,
    ):
        await super()._aenter()  # type: ignore

        self._pair = pair
        self._fetch_limit = fetch_limit
        self._amount_limit = amount_limit

    async def _gather(self) -> None:
        window: Window = Window()

        for i in range(self._fetch_limit):

            def log(message: str, extra: dict = {}):
                logger.info(
                    message,
                    extra={
                        "kind": "Streamer",
                        "exchange": self.exchange.name,
                        "pair": self._pair,
                        "index": i,
                        "limit": self._fetch_limit,
                        **extra,
                    },
                )

            log("request")
            response: dict = await self._cryptoxlib_client.get_historical_trades(
                pair=self._pair, limit=self._amount_limit, from_id=window.next_id
            )

            try:
                body: dict = response["response"]
                window = Window.from_response(body, self._amount_limit)
            except (KeyError, IndexError) as e:
                log("malformed response")
                raise e

            log("response", {"window": window})

            for t in body:
                await self._queue.put(BinanceTrade.from_http_api(self._pair, t))

        self._complete: bool = True


@attr.s(auto_attribs=True)
class BinanceFetcher(Fetcher):
    exchange: Exchange = Exchange.binance
    create_client: Callable = CryptoXLib.create_binance_client
