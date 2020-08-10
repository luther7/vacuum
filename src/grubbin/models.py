from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Candle:
    # https://github.com/binance-exchange/binance-official-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
    #
    # {
    #   "e": "kline",     // Event type
    #   "E": 123456789,   // Event time
    #   "s": "BNBBTC",    // Symbol
    #   "k": {
    #     "t": 123400000, // Kline start time
    #     "T": 123460000, // Kline close time
    #     "s": "BNBBTC",  // Symbol
    #     "i": "1m",      // Interval
    #     "f": 100,       // First trade ID
    #     "L": 200,       // Last trade ID
    #     "o": "0.0010",  // Open price
    #     "c": "0.0020",  // Close price
    #     "h": "0.0025",  // High price
    #     "l": "0.0015",  // Low price
    #     "v": "1000",    // Base asset volume
    #     "n": 100,       // Number of trades
    #     "x": false,     // Is this kline closed?
    #     "q": "1.0000",  // Quote asset volume
    #     "V": "500",     // Taker buy base asset volume
    #     "Q": "0.500",   // Taker buy quote asset volume
    #     "B": "123456"   // Ignore
    #   }
    # }
    event_time: int
    stream: str
    symbol: str
    kline_start_time: int
    kline_close_time: int
    interval: str
    first_trade_id: int
    last_trade_id: int
    open_price: Decimal
    close_price: Decimal
    high_price: Decimal
    low_price: Decimal
    base_asset_volume: Decimal
    number_of_trades: int
    closed: bool
    quote_asset_volume: Decimal
    taker_buy_base_asset_volume: Decimal
    taker_buy_quote_asset_volume: Decimal

    @classmethod
    def from_ws_api(cls, response: dict) -> "Candle":
        return cls(
            event_time=int(response["data"]["E"]),
            stream=response["stream"],
            symbol=response["data"]["s"],
            kline_start_time=int(response["data"]["k"]["t"]),
            kline_close_time=int(response["data"]["k"]["T"]),
            interval=response["data"]["k"]["i"],
            first_trade_id=int(response["data"]["k"]["f"]),
            last_trade_id=int(response["data"]["k"]["L"]),
            open_price=Decimal(response["data"]["k"]["o"]),
            close_price=Decimal(response["data"]["k"]["c"]),
            high_price=Decimal(response["data"]["k"]["h"]),
            low_price=Decimal(response["data"]["k"]["l"]),
            base_asset_volume=Decimal(response["data"]["k"]["v"]),
            number_of_trades=int(response["data"]["k"]["n"]),
            closed=bool(response["data"]["k"]["x"]),
            quote_asset_volume=Decimal(response["data"]["k"]["q"]),
            taker_buy_base_asset_volume=Decimal(response["data"]["k"]["V"]),
            taker_buy_quote_asset_volume=Decimal(response["data"]["k"]["Q"]),
        )
