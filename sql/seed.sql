CREATE DATABASE grubbin;

\connect grubbin;

CREATE TABLE binance_trade (
  id                  bigint   NOT NULL,
  time                bigint   NOT NULL,
  price               decimal  NOT NULL,
  symbol              text     NOT NULL,
  quantity            decimal  NOT NULL,
  buyer_order_id      bigint   NOT NULL,
  seller_order_id     bigint   NOT NULL,
  trade_time          bigint   NOT NULL,
  buyer_market_maker  bigint   NOT NULL
);

CREATE INDEX ON binance_trade (time);

CREATE TABLE bitforex_trade (
  id         bigint   NOT NULL,
  time       bigint   NOT NULL,
  price      decimal  NOT NULL,
  amount     bigint   NOT NULL,
  direction  bigint   NOT NULL
);

CREATE INDEX ON bitforex_trade (time);
