# Grub's Bin-Bot
![Tests](https://github.com/rubberydub/grub-bin-bot/workflows/tests/badge.svg)

---

## TODO

- Stored procedures?

## Requires
- Minikube
- Poetry
- Binance API Key


## Usage

- Provsions Minikube with Postgres and Grafana, and forward ports
```
scripts/reprovision
```

- Run script to pull Candle data and push to InfluxDB:
```
poetry run grubbin run --binance-api-key=SNIP --binance-security-key=SNIP
```

- Log into Grafana at `localhost:3000` (username: admin, password: password).
