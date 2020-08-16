from asyncio import Queue, gather, sleep
from typing import Callable, Optional

import attr
from asyncpg import Connection
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.CryptoXLibClient import CryptoXLibClient
from cryptoxlib.Pair import Pair

from .config import config

# from .config import config, pairs
from .logger import get_logger
from .models import BinanceTrade, Exchange, Trade, as_postgres_row
from .postgres import get_postgres_connection

logger = get_logger(__name__)


async def fetch() -> None:
    # async with BinanceFetcher() as binance, BitforexFetcher() as bitforex:
    #     await gather(binance.run(), bitforex.run())

    async with BinanceFetcher() as binance:
        await gather(binance.run())


@attr.s(auto_attribs=True)
class Fetcher:
    exchange: Exchange
    create_client: Callable

    _cryptoxlib_client: CryptoXLibClient = None
    _postgres_connection: Connection = None
    _queue: Queue = attr.ib(factory=Queue)
    _complete: bool = False

    _queue_size: int = 1000

    _fetch_limit: int = 1
    _amount_limit: int = 1

    async def __aenter__(self, fetch_limit: int = 5, amount_limit: int = 1000):
        self._fetch_limit = fetch_limit
        self._amount_limit = amount_limit

        self._queue = Queue(self._queue_size)
        self._postgres_connection = await get_postgres_connection()

        self._cryptoxlib_client: CryptoXLibClient = self.create_client(
            config["exchanges"][self.exchange.name]["api_key"],
            config["exchanges"][self.exchange.name]["security_key"],
        )

        return self

    async def __aexit__(self, *args, **kwargs):
        await self._cryptoxlib_client.close()
        await self._postgres_connection.close()

    async def _fetch(self) -> None:
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
        - Fetch historical data from the exchange.
        - Parse and enqueue messages from the response.
        - Feed the queued messaged into Postgres.
        """
        await gather(self._fetch(), self._insert())


@attr.s(auto_attribs=True)
class BinanceFetcher(Fetcher):
    exchange: Exchange = Exchange.binance
    create_client: Callable = CryptoXLib.create_binance_client
