from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class State:
    start_time: datetime
    streaming: bool = False
    fetching: bool = False
    postgres: bool = False
    streaming_error: Optional[str] = None
    fetching_error: Optional[str] = None
    postgres_error: Optional[str] = None

    @classmethod
    def new(cls) -> "State":
        return cls(start_time=datetime.now())


state: State = State.new()
