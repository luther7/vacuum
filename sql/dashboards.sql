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
  max(candles.high) AS high,
  max(candles.low) AS low,
  max(candles.open) AS open,
  max(candles.close) AS close
FROM
  candles
GROUP BY
  time
ORDER BY
  time
