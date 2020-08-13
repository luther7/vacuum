from asyncio import Queue

from .models import BinanceTrade


async def parse_trade(response: dict, queue: Queue) -> None:
    print("Parsing Binance Trade")
    queue.put_nowait(BinanceTrade.from_ws_api(response))
