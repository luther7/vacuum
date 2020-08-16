# Grub's Bin-Bot
![Tests](https://github.com/rubberydub/grub-bin-bot/workflows/tests/badge.svg)

---

## TODO

- Fix stop endpoint and stream task
- Add endpoint for fetching historical data
- Docker/Kube/Skaffold
- Automate Grafana Dashboards


## Requires
- Minikube
- Poetry
- Binance API Key
- Bitforex API Key


## Usage

- Prepare Helm Charts:
```
scripts/prepare-charts
```

- Provsions Minikube with TimescaleDB and Grafana, and forward ports:
```
scripts/reprovision
```

- Run script to pull Candle data and push to Timescale:
```
poetry run grubbin run
```

- Log into Grafana at `localhost:3000` (username: admin, password: password).
