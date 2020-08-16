from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from .config import config, root

SQL_DIR: str = "sql"
SCHEMA_FILE: str = "schema.sql"


def schema() -> None:
    path: Path = (root / SQL_DIR).resolve(strict=True)
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(f"{SCHEMA_FILE}.j2")

    rendered = template.render(
        exchanges=config["exchanges"].keys(),
        aggregation_intervals=config["aggregation_intervals"],
    )

    with open(path / SCHEMA_FILE, "w") as f:
        f.write(rendered)
