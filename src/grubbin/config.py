from pathlib import Path
from typing import List

import yaml
from cryptoxlib.Pair import Pair

root: Path = Path(__file__).resolve().parent.parent.parent
path: Path = (root / "config.yaml").resolve(strict=True)

with open(path, "r") as f:
    config: dict = yaml.safe_load(f)

pairs: List[Pair] = [Pair(p.split("/")[0], p.split("/")[1]) for p in config["pairs"]]
