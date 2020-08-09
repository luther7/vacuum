# Grub's Bin-Bot
![Tests](https://github.com/rubberydub/grub-bin-bot/workflows/tests/badge.svg)

---

## TODO

### For pylate:
- [ ] Remove CD's in actions
- [ ] Simplify directory structure
- [ ] Add main module

### For grubbin:
- [ ] Structured logging


## Requires
- Minikube
- Poetry
- Binance API Key


## Usage

- Start Minikube and install InfluxDB and Grafana:
```
scripts/minikube-start
scripts/install-monitoring
```

- Open a new terminal and forward a port to the Grafana Service:
```
forward-grafana-port
```

- Open a new terminal and forward a port to the InfluxDB Service:
```
forward-influxdb-port
```

- Run script to pull Candle data and push to InfluxDB:
```
poetry run grubbin run --binance-api-key=SNIP --binance-security-key=SNIP
```

- Log into Grafana at `localhost:3000` (username: admin, password: password).
- Dashboard is called BTCUSTD.
