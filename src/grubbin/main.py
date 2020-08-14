from asyncio import gather

from .logger import get_logger
from .streamer import BinanceStreamer, BitforexStreamer

logger = get_logger(__name__)


async def stream() -> None:
    async with BinanceStreamer() as binance, BitforexStreamer() as bitforex:
        await gather(binance.run(), bitforex.run())
