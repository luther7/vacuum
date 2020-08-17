# Grub's Bin-Bot
![Tests](https://github.com/rubberydub/grub-bin-bot/workflows/tests/badge.svg)

---

## TODO
- Fix Timescale secrets
- Rename - `grub-bin-bot` and `grubbin` to `vacuum`
- Add the config as a configmap in the Helm chart
- Fix stop endpoint
- Fix stream task to handle stops
- Add endpoint for fetching historical data
- Automate Grafana Dashboards


## Requires
- Minikube
- Kubectl
- Kustomize
- Skaffold
- Poetry
- Binance API Key
- Bitforex API Key


## Usage

- Prepare Helm Charts:
```
scripts/prepare-charts
```

- Provsions Minikube, deploys Kubernetes resources with Skaffold and forwards ports:
```
scripts/reprovision
```

- Seed the database:
```
scripts/seed-database
```

- Interact via HTTP API:
```
http localhost:5000/start
http localhost:5000/stop
http localhost:5000/status
```

- Log into Grafana at `localhost:3000` (username: admin, password: password).
