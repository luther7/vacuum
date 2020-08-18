# Vacuum
![Tests](https://github.com/rubberydub/vacuum/workflows/tests/badge.svg)

---

## TODO
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
cp config-example.yaml config
$EDITOR config.yaml
```

Prepare Helm Charts:
```
./scripts/prepare-charts
```

Provsion Minikube, deploy Kubernetes resources with Skaffold, forwards ports:
```
./scripts/reprovision
```

Seed the database:
```
./scripts/seed-database
```

Interact via HTTP API:
```
http localhost:5000/start
http localhost:5000/stop
http localhost:5000/status
```

Log into Grafana at `localhost:3000` (username: admin, password: password).

More scripts in `./scripts`
