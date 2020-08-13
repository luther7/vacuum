WITH klines AS (
  SELECT
    kline_start_time AS start_time,
    kline_close_time AS close_time,
    max(high_price) AS high,
    min(low_price) AS low
  FROM
    candles
  WHERE
    kline_start_time >= $__unixEpochFrom()
  AND
    kline_close_time <= $__unixEpochTo()
  GROUP BY
    kline_start_time, kline_close_time
)
SELECT
  generate_series(klines.start_time/1000, klines.close_time/1000) AS time,
  max(klines.high) AS high,
  max(klines.low) AS low,
  (
    SELECT
      open_price
    FROM
      candles
    WHERE
      start_time = klines.start_time
    ORDER BY
      event_time ASC
    LIMIT
      1
  ) AS open,
  (
    SELECT
      close_price
    FROM
      candles
    WHERE
      close_time = klines.close_time
    ORDER BY
      event_time DESC
    LIMIT
      1
  ) AS close
FROM
  klines
GROUP BY
  time
ORDER BY
  time
