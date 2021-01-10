# Vacuum ![Tests](https://github.com/rubberydub/vacuum/workflows/tests/badge.svg)

Crypto trading bot. Uses Python, Tulip Indicators (TODO), TimescaleDB, Grafana and Kubernetes.

## WORK IN PROGRESS

In it's current state, Vacuum will consume real-time trading data from Binance and Bitforex, and
can fetch historical data from Binance. It is controlled with a HTTP API. It will insert this data
into TimescaleDB, including continuous aggregations. The trading data is visualized in Grafana.
These features are almost complete, with the remaining work listed below.

Future features include using Tulip Indicators to build trading algorithms, and a mock wallet and
visualizations to test them.

## TODO

- Automate provisioning of Grafana Dashboards
- Add API endpoint for fetching historical data
- Unit tests when existing Python modules stabilize

## Future Features

- Mock wallet
- Tulip Indicators
- Trading using mock wallet and tulip indicators
- Integrate more exchanges

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
