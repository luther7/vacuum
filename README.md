# Vacuum
![Tests](https://github.com/rubberydub/vacuum/workflows/tests/badge.svg)

---

## TODO
- Add JSON error handler to API
- Fix stream task to handle stops
- Fix stop endpoint
- Automate Grafana Dashboards
- Add endpoint for fetching historical data


## Requires
- Minikube
- Kubectl
- Skaffold
- Binance API Key
- Bitforex API Key


## Usage

Copy and edit the example config:
```
cp config-example.yaml config.yaml
$EDITOR config.yaml
```

Prepare Helm Charts:
```
./scripts/prepare-charts
```

Start Minikube:
```
./scripts/minikube-start
```

Deploy with Skaffold and forwards ports:
```
./scripts/skaffold-dev
```

Seed the database:
```
./scripts/seed-database
```

Log into Grafana at `localhost:3000` (username: admin, password: password).

Interact via the HTTP API:
```
http localhost:5000/start
http localhost:5000/stop
http localhost:5000/status
```

More scripts in `./scripts`
