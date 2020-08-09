from asyncio import Queue
from typing import Any, Callable, List

from cryptoxlib.clients.binance.BinanceWebsocket import BinanceSubscription
from cryptoxlib.clients.binance.functions import map_ws_pair
from cryptoxlib.Pair import Pair

from .models import Candle


class CandlesSubscription(BinanceSubscription):
    def __init__(self, pair: Pair, callbacks: List[Callable[[dict], Any]]):
        super().__init__(callbacks)

        self.pair = pair

    def get_channel_name(self) -> str:
        return f"{map_ws_pair(self.pair)}@kline_1m"


async def parse_candle(response: dict, queue: Queue) -> None:
    print("Parsing candle")
    queue.put_nowait(Candle.from_ws_api(response))
