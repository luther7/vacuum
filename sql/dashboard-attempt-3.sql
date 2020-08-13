SELECT
  c.start_time AS start_time,
  max(c.close_time) AS close_time,
  max(c.open) AS open,
  max(c.close) AS close
FROM (
  SELECT
    kline_start_time AS start_time,
    kline_close_time AS close_time,
    first_value(open_price) OVER (PARTITION BY kline_start_time ORDER BY event_time) AS open,
    last_value(close_price) OVER (PARTITION BY kline_start_time ORDER BY event_time) AS close
  FROM
    candles
) AS c
GROUP BY
  c.start_time

SELECT
  c.start_time AS start_time,
  max(c.close_time) AS close_time,
  max(c.open) AS open,
  max(c.close) AS close
FROM (
  SELECT
    kline_start_time AS start_time,
    kline_close_time AS close_time,
    first_value(open_price) OVER (PARTITION BY kline_start_time ORDER BY event_time) AS open,
    last_value(close_price) OVER (PARTITION BY kline_start_time ORDER BY event_time) AS close
  FROM
    candles
) AS c
GROUP BY
  c.start_time

  --
WITH klines AS (
  SELECT
    c.start_time AS start_time,
    c.close_time AS close_time,
    c.open AS open,
    c.close AS close
    c.high AS high,
    c.low AS low
  FROM (
    SELECT
      kline_start_time AS start_time,
      kline_close_time AS close_time,
      first_value(open_price) OVER (PARTITION BY kline_start_time ORDER BY event_time) AS open,
      last_value(close_price) OVER (PARTITION BY kline_start_time ORDER BY event_time ASC) AS close,
    FROM
      candles
  ) AS c
)
SELECT
  generate_series(klines.start_time/1000, klines.close_time/1000) AS time,
  max(klines.open) AS open,
  max(klines.close) AS close
  max(klines.high) AS open,
  max(klines.low) AS close
FROM
  klines
GROUP BY
  time
ORDER BY
  time




  --- FUCK

  WITH klines AS (
      SELECT
          kline_start_time AS start_time,
              max(kline_close_time) AS close_time,
                  max(open_price) AS open,
                      max(close_price) AS close,
                          max(high_price) AS high,
                              min(low_price) AS low
                                FROM
                                    candles
                                      GROUP BY
                                          kline_start_time
                                        )
                                        SELECT
                                          generate_series(klines.start_time/1000, klines.close_time/1000) AS time,
                                            max(klines.open) AS open,
                                              max(klines.close) AS close
                                              FROM
                                                klines
                                                GROUP BY
                                                  time
                                                  ORDER BY
                                                    time
