from datetime import datetime
from decimal import Decimal
from enum import Enum

import attr

from .utilities import epoch_ms_to_datetime


class Exchange(Enum):
    binance = 1
    bitforex = 2


@attr.s(auto_attribs=True)
class Trade:
    """
    The order of attributes must match the order of the Postgres columns.
    """

    exchange: Exchange
    time: datetime
    id: int
    ingestion_time: datetime
    price: Decimal
    quantity: Decimal


def as_postgres_row(trade: Trade) -> tuple:
    """
    The exchange enum is not inserted.
    """

    return attr.astuple(trade)[:-1]


@attr.s(auto_attribs=True)
class BinanceTrade(Trade):
    """
    The order of attributes must match the order of the Postgres columns.

    https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#aggregate-trade-streams

    {
      "e": "trade",     // Event type
      "E": 123456789,   // Event time
      "s": "BNBBTC",    // Symbol
      "t": 12345,       // Trade ID
      "p": "0.001",     // Price
      "q": "100",       // Quantity
      "b": 88,          // Buyer order ID
      "a": 50,          // Seller order ID
      "T": 123456785,   // Trade time
      "m": true,        // Is the buyer the market maker?
      "M": true         // Ignore
    }
    """

    symbol: str
    buyer_order_id: int
    seller_order_id: int
    trade_time: int
    buyer_market_maker: bool

    exchange: Exchange = Exchange.binance

    @classmethod
    def from_websocket_api(cls, response: dict) -> "BinanceTrade":
        return cls(
            time=epoch_ms_to_datetime(response["E"]),
            id=int(response["t"]),
            ingestion_time=datetime.now(),
            price=Decimal(response["p"]),
            quantity=Decimal(response["q"]),
            symbol=response["s"],
            buyer_order_id=int(response["b"]),
            seller_order_id=int(response["a"]),
            trade_time=int(response["T"]),
            buyer_market_maker=bool(response["m"]),
        )


@attr.s(auto_attribs=True)
class BitforexTrade(Trade):
    """
    The order of attributes must match the order of the Postgres columns.

    https://github.com/githubdev2020/API_Doc_en/wiki/Trading-record-information

    {
        "success": true,
        "data": [{
            "amount": 1,
            "direction": 1,
            "price": 990,
            "tid": "8076",
            "time": 1516628489676
        }]
    }
    """

    direction: int

    exchange: Exchange = Exchange.bitforex

    @classmethod
    def from_websocket_api(cls, response: dict) -> "BitforexTrade":
        return cls(
            time=epoch_ms_to_datetime(response["time"]),
            id=int(response["tid"]),
            ingestion_time=datetime.now(),
            price=Decimal(response["price"]),
            quantity=Decimal(response["amount"]),
            direction=int(response["direction"]),
        )
