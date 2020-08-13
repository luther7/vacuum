from asyncio import Queue

from .logger import get_logger
from .models import BinanceTrade

logger = get_logger(__name__)


async def parse_trade(response: dict, queue: Queue) -> None:
    logger.info("Parsing Binance Trade")
    queue.put_nowait(BinanceTrade.from_ws_api(response))
