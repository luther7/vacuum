from pathlib import Path

import yaml
from cryptoxlib.Pair import Pair

root: Path = Path(__file__).resolve().parent.parent.parent
path: Path = (root / "config.yaml").resolve(strict=True)

with open(path, "r") as f:
    config: dict = yaml.safe_load(f)

default_pair: Pair = Pair("BTC", "USDT")
