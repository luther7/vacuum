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
    id: int
    time: int
    price: Decimal
    symbol: str
    quantity: Decimal
    buyer_order_id: int
    seller_order_id: int
    trade_time: int
    buyer_market_maker: bool

    @classmethod
    def from_ws_api(cls, response: dict) -> "BinanceTrade":
        return cls(
            id=int(response["t"]),
            time=int(response["E"]),
            price=Decimal(response["p"]),
            symbol=response["s"],
            quantity=Decimal(response["q"]),
            buyer_order_id=int(response["b"]),
            seller_order_id=int(response["a"]),
            trade_time=int(response["T"]),
            buyer_market_maker=bool(response["m"]),
        )


@dataclass
class BitforexTrade:
    # https://github.com/githubdev2020/API_Doc_en/wiki/Trading-record-information
    #
    # {
    # 	"success": true,
    # 	"data": [{
    # 		"amount": 1,
    # 		"direction": 1,
    # 		"price": 990,
    # 		"tid": "8076",
    # 		"time": 1516628489676
    # 	}]
    # }
    id: int
    time: int
    price: Decimal
    amount: int
    direction: int

    @classmethod
    def from_ws_api(cls, response: dict) -> "BitforexTrade":
        return cls(
            id=int(response["tid"]),
            time=int(response["time"]),
            price=Decimal(response["price"]),
            amount=int(response["amount"]),
            direction=int(response["direction"]),
        )
