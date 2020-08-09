from datetime import datetime


def _timestamp(time: int) -> str:
    return datetime.utcfromtimestamp(time / 1000).strftime("%Y-%m-%dT%H:%M:%SZ")
