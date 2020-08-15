---
--- seed.sql
---

CREATE DATABASE grubbin;

\connect grubbin;

--
-- UDFs
--

CREATE FUNCTION seconds_in_minute_preceding(TIMESTAMPTZ)
RETURNS SETOF TIMESTAMPTZ
LANGUAGE SQL STABLE AS $$
  SELECT generate_series($1 - INTERVAL '59 seconds', $1, INTERVAL '1 second')
$$;

CREATE FUNCTION seconds_in_minute_succeeding(TIMESTAMPTZ)
RETURNS SETOF TIMESTAMPTZ
LANGUAGE SQL STABLE AS $$
  SELECT generate_series($1, $1 + INTERVAL '59 seconds', INTERVAL '1 second')
$$;

---
--- binance
---

CREATE TABLE binance_trade (
  time                TIMESTAMPTZ  NOT NULL,
  id                  BIGINT       NOT NULL,
  ingestion_time      TIMESTAMPTZ  NOT NULL,
  price               DECIMAL      NOT NULL,
  quantity            DECIMAL      NOT NULL,
  symbol              TEXT         NOT NULL,
  buyer_order_id      BIGINT       NOT NULL,
  seller_order_id     BIGINT       NOT NULL,
  trade_time          BIGINT       NOT NULL,
  buyer_market_maker  BIGINT       NOT NULL,
  PRIMARY KEY(time, id)
);

CREATE INDEX ON binance_trade (time, quantity, price);

SELECT create_hypertable('binance_trade', 'time');

CREATE VIEW binance_trade_candles_1m
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '1 minute', time) AS minute,
  count(*)                               AS data_points,
  sum(quantity)                          AS volume,
  min(price)                             AS low,
  max(price)                             AS high,
  first(price, time)                     AS open,
  last(price, time)                      AS close
FROM binance_trade
GROUP BY minute;

---
--- bitforex
---

CREATE TABLE bitforex_trade (
  time            TIMESTAMPTZ  NOT NULL,
  id              BIGINT       NOT NULL,
  ingestion_time  TIMESTAMPTZ  NOT NULL,
  price           DECIMAL      NOT NULL,
  quantity        BIGINT       NOT NULL,
  direction       BIGINT       NOT NULL,
  PRIMARY KEY(time, id, ingestion_time)
);

CREATE INDEX ON bitforex_trade (time, quantity, price);

SELECT create_hypertable('bitforex_trade', 'time');

CREATE VIEW bitforex_trade_candles_1m
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '1 minute', time) AS minute,
  count(*)                               AS data_points,
  sum(quantity)                          AS volume,
  min(price)                             AS low,
  max(price)                             AS high,
  first(price, time)                     AS open,
  last(price, time)                      AS close
FROM bitforex_trade
GROUP BY minute;
