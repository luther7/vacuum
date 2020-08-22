from dataclasses import dataclass
from datetime import datetime


@dataclass
class State:
    start_time: datetime
    streaming: bool = False
    fetching: bool = False

    @classmethod
    def new(cls) -> "State":
        return cls(start_time=datetime.now())


state: State = State.new()
