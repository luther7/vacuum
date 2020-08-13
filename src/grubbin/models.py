from dataclasses import dataclass
from decimal import Decimal


@dataclass
class BinanceTrade:
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#aggregate-trade-streams
    #
    # {
    #   "e": "trade",     // Event type
    #   "E": 123456789,   // Event time
    #   "s": "BNBBTC",    // Symbol
    #   "t": 12345,       // Trade ID
    #   "p": "0.001",     // Price
    #   "q": "100",       // Quantity
    #   "b": 88,          // Buyer order ID
    #   "a": 50,          // Seller order ID
    #   "T": 123456785,   // Trade time
    #   "m": true,        // Is the buyer the market maker?
    #   "M": true         // Ignore
    # }
    trade_id: int
    event_time: int
    symbol: str
    price: Decimal
    quantity: Decimal
    buyer_order_id: int
    seller_order_id: int
    trade_time: int
    buyer_market_maker: bool

    @classmethod
    def from_ws_api(cls, response: dict) -> "BinanceTrade":
        return cls(
            trade_id=int(response["data"]["t"]),
            event_time=int(response["data"]["E"]),
            symbol=response["data"]["s"],
            price=Decimal(response["data"]["p"]),
            quantity=Decimal(response["data"]["q"]),
            buyer_order_id=int(response["data"]["b"]),
            seller_order_id=int(response["data"]["a"]),
            trade_time=int(response["data"]["T"]),
            buyer_market_maker=bool(response["data"]["m"]),
        )
