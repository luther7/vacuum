import logging
from datetime import datetime

from cryptoxlib.clients.binance.BinanceWebsocket import (
    AccountSubscription,
    BestOrderBookSymbolTickerSubscription,
    BestOrderBookTickerSubscription,
    TradeSubscription,
)
from cryptoxlib.CryptoXLib import CryptoXLib
from cryptoxlib.Pair import Pair

LOG = logging.getLogger("cryptoxlib")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())


async def account_update(response: dict) -> None:
    print(f"Callback account_update: [{response}]")


async def order_book_update(response: dict) -> None:
    print(f"Callback order_book_update: [{response}]")


async def trade_update(response: dict) -> None:
    local_timestamp_ms = int(datetime.now().timestamp() * 1000)
    server_timestamp_ms = response["data"]["E"]
    print(
        f"Callback trade_update: trade update timestamp diff [ms]:"
        f" {local_timestamp_ms - server_timestamp_ms}"
    )


async def orderbook_ticker_update(response: dict) -> None:
    print(f"Callback orderbook_ticker_update: [{response}]")


async def run(api_key: str, sec_key: str) -> None:
    client = CryptoXLib.create_binance_client(api_key, sec_key)

    # Bundle several subscriptions into a single websocket
    client.compose_subscriptions(
        [
            BestOrderBookTickerSubscription(callbacks=[orderbook_ticker_update]),
            BestOrderBookSymbolTickerSubscription(
                pair=Pair("BTC", "USDT"), callbacks=[orderbook_ticker_update]
            ),
            TradeSubscription(pair=Pair("ETH", "BTC"), callbacks=[trade_update]),
        ]
    )

    # Bundle another subscriptions into a separate websocket
    client.compose_subscriptions([AccountSubscription(callbacks=[account_update])])

    # Execute all websockets asynchronously
    await client.start_websockets()

    await client.close()
