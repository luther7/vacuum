from datetime import datetime


def epoch_ms_to_datetime(time: int) -> datetime:
    return datetime.fromtimestamp(time / 1000)
