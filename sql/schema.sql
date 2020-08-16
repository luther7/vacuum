/* vim: set filetype=sql : */

---
--- schema.sql
---

CREATE DATABASE grubbin;

\connect grubbin;


--
-- UDFs
--

CREATE FUNCTION seconds_in_minute_preceding(TIMESTAMPTZ)
RETURNS SETOF TIMESTAMPTZ
LANGUAGE SQL STABLE AS $$
  SELECT generate_series($1 - '59 seconds', $1, '1 second')
$$;

CREATE FUNCTION seconds_in_minute_succeeding(TIMESTAMPTZ)
RETURNS SETOF TIMESTAMPTZ
LANGUAGE SQL STABLE AS $$
  SELECT generate_series($1, $1 + INTERVAL '59 seconds', INTERVAL '1 second')
$$;


---
--- Base tables
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

CREATE TABLE bitforex_trade (
  time            TIMESTAMPTZ  NOT NULL,
  id              BIGINT       NOT NULL,
  ingestion_time  TIMESTAMPTZ  NOT NULL,
  price           DECIMAL      NOT NULL,
  quantity        BIGINT       NOT NULL,
  direction       BIGINT       NOT NULL,
  PRIMARY KEY(time, id, ingestion_time)
);


--
-- Views
--

CREATE INDEX ON binance_trade (time, quantity, price);

SELECT create_hypertable('binance_trade', 'time');

CREATE VIEW binance_trade_aggregations_1_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '1 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM binance_trade
GROUP BY _time;

CREATE VIEW binance_trade_aggregations_3_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '3 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM binance_trade
GROUP BY _time;

CREATE VIEW binance_trade_aggregations_5_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '5 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM binance_trade
GROUP BY _time;

CREATE VIEW binance_trade_aggregations_10_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '10 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM binance_trade
GROUP BY _time;

CREATE VIEW binance_trade_aggregations_30_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '30 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM binance_trade
GROUP BY _time;

CREATE INDEX ON bitforex_trade (time, quantity, price);

SELECT create_hypertable('bitforex_trade', 'time');

CREATE VIEW bitforex_trade_aggregations_1_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '1 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM bitforex_trade
GROUP BY _time;

CREATE VIEW bitforex_trade_aggregations_3_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '3 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM bitforex_trade
GROUP BY _time;

CREATE VIEW bitforex_trade_aggregations_5_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '5 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM bitforex_trade
GROUP BY _time;

CREATE VIEW bitforex_trade_aggregations_10_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '10 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM bitforex_trade
GROUP BY _time;

CREATE VIEW bitforex_trade_aggregations_30_minutes
WITH (timescaledb.continuous) AS
SELECT
  time_bucket(INTERVAL '30 minutes', time)  AS _time,
  count(*)                                      AS _count,
  sum(quantity)                                 AS _sum,
  min(price)                                    AS _min,
  max(price)                                    AS _max,
  first(price, time)                            AS _first,
  last(price, time)                             AS _last,
  avg(price)                                    AS _avg,
  stddev(price)                                 AS _stddev,
  stddev_pop(price)                             AS _stddev_pop,
  stddev_samp(price)                            AS _stddev_samp,
  variance(price)                               AS _variance,
  var_pop(price)                                AS _var_pop,
  var_samp(price)                               AS _var_samp
FROM bitforex_trade
GROUP BY _time;
