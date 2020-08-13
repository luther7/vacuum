from asyncio import Queue

from .logger import get_logger
from .models import BinanceTrade, BitforexTrade

logger = get_logger(__name__)


async def parse_binance_trade(response: dict, queue: Queue) -> None:
    logger.info("Received", extra={"exchange": "binance"})

    queue.put_nowait(BinanceTrade.from_ws_api(response["data"]))


async def parse_bitforex_trade(response: dict, queue: Queue) -> None:
    logger.info("Received", extra={"exchange": "bitforex"})

    for t in response["data"]:
        queue.put_nowait(BitforexTrade.from_ws_api(t))
