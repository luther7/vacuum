CREATE TABLE candles (
  event_time                    bigint   PRIMARY KEY,
  stream                        text     NOT NULL,
  symbol                        text     NOT NULL,
  kline_start_time              bigint   NOT NULL,
  kline_close_time              bigint   NOT NULL,
  interval                      text     NOT NULL,
  first_trade_id                bigint   NOT NULL,
  last_trade_id                 bigint   NOT NULL,
  open_price                    decimal  NOT NULL,
  close_price                   decimal  NOT NULL,
  high_price                    decimal  NOT NULL,
  low_price                     decimal  NOT NULL,
  base_asset_volume             decimal  NOT NULL,
  number_of_trades              bigint   NOT NULL,
  closed                        boolean  NOT NULL,
  quote_asset_volume            decimal  NOT NULL,
  taker_buy_base_asset_volume   decimal  NOT NULL,
  taker_buy_quote_asset_volume  decimal  NOT NULL
);

CREATE INDEX ON candles (kline_start_time);

CREATE INDEX ON candles (kline_close_time);
