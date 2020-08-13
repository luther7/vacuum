CREATE TABLE binance_trade (
  trade_id            bigint   PRIMARY KEY,
  event_time          bigint   NOT NULL,
  symbol              text     NOT NULL,
  price               decimal  NOT NULL,
  quantity            decimal  NOT NULL,
  buyer_order_id      bigint   NOT NULL,
  seller_order_id     bigint   NOT NULL,
  trade_time          bigint   NOT NULL,
  buyer_market_maker  bigint   NOT NULL
);

CREATE INDEX ON binance_trade (event_time);
