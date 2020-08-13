WITH candles AS (
  SELECT
    DISTINCT(floor(event_time/1000/60)::int * 60) AS start_time,
    max(price) OVER (PARTITION BY floor(event_time/1000/60)::int * 60) AS high,
    min(price) OVER (PARTITION BY floor(event_time/1000/60)::int * 60) AS low,
    first_value(price) OVER (PARTITION BY floor(event_time/1000/60)::int * 60) AS open,
    last_value(price) OVER (PARTITION BY floor(event_time/1000/60)::int * 60) AS close
  FROM
    binance_trade
  WHERE
    event_time/1000 >= $__unixEpochFrom()
  AND
    event_time/1000 <= $__unixEpochTo()
)
SELECT
  generate_series(candles.start_time, (candles.start_time+60)) AS time,
  max(candles.high) AS c_high,
  max(candles.low) AS c_low,
  max(candles.open) AS c_open,
  max(candles.close) AS c_close
FROM
  candles
GROUP BY
  time
ORDER BY
  time

WITH averages AS (
  SELECT
    DISTINCT(floor(event_time/1000/60)::int * 60) AS time,
    avg(price) OVER (PARTITION BY floor(event_time/1000/60)::int * 60) AS price,
  FROM
    binance_trade
  WHERE
    event_time/1000 >= $__unixEpochFrom()
  AND
    event_time/1000 <= $__unixEpochTo()
),
bollinger_bands_21_2 AS (
  SELECT
    time AS time,
    avg(price) OVER (ORDER BY time ROWS 20 PRECEDING) AS average,
    avg(price) OVER (ORDER BY time ROWS 20 PRECEDING)
      + (stddev(price) OVER (ORDER BY time ROWS 20 PRECEDING)*2) AS high,
    avg(price) OVER (ORDER BY time ROWS 20 PRECEDING)
      - (stddev(price) OVER (ORDER BY time ROWS 20 PRECEDING)*2) AS low
  FROM
    averages
)
SELECT
  bollinger_bands_21_2.time AS time,
  max(bollinger_bands_21_2.average) AS bb_average,
  max(bollinger_bands_21_2.high) AS bb_high,
  max(bollinger_bands_21_2.low) AS bb_low
FROM
  bollinger_bands_21_2
GROUP BY
  time
ORDER BY
  time
