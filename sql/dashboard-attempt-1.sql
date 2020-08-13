WITH kline AS (
  SELECT
    kline_start_time as target
  FROM
    candles
  WHERE
    kline_start_time <= 1597059840000
  ORDER BY
    event_time DESC
  LIMIT
    1
),
seconds AS (
  SELECT
    generate_series(kline_start_time/1000, kline_close_time/1000) AS time
  FROM
    candles
  WHERE
    kline_start_time = (SELECT target FROM kline)
),
high_low AS (
  SELECT
    max(high_price) AS high,
    min(low_price) AS low
  FROM
    candles
  WHERE
    kline_start_time = (SELECT target FROM kline)
),
open AS (
  SELECT
    open_price AS open
  FROM
    candles
  WHERE
    kline_start_time = (SELECT target FROM kline)
  ORDER BY
    event_time ASC
  LIMIT
    1
),
close AS (
  SELECT
    close_price AS close
  FROM
    candles
  WHERE
    kline_start_time = (SELECT target FROM kline)
  ORDER BY
    event_time DESC
  LIMIT
    1
)
SELECT
  seconds.time AS time,
  high_low.high AS high,
  high_low.low AS low,
  open.open AS open,
  close.close AS close
FROM
  seconds,
  high_low,
  open,
  close
