from asyncio import AbstractEventLoop, get_event_loop
from dataclasses import asdict, dataclass
from datetime import datetime

from quart import Quart

from .logger import get_logger
from .streamer import stream

logger = get_logger(__name__)
app = Quart(__name__)


@dataclass
class State:
    started: datetime
    streaming: bool = False
    fetching: bool = False

    @classmethod
    def new(cls) -> "State":
        return cls(started=datetime.now())


state: State = State.new()


@app.route("/healthz", methods=["GET"])
async def healthz():
    return "", 200


@app.route("/status", methods=["GET"])
async def status():
    return asdict(state)


@app.route("/start", methods=["POST"])
async def start():
    logger.info("starting")

    if not state.streaming:
        loop: AbstractEventLoop = get_event_loop()
        loop.create_task(stream())
        state.streaming = True

    return {"success": True}


@app.route("/stop", methods=["POST"])
async def stop():
    logger.info("stopping")

    if state.streaming:
        loop: AbstractEventLoop = get_event_loop()
        loop.stop()
        loop.close()
        state.streaming = False

    return {"success": True}


def webserver() -> None:
    app.run(host="0.0.0.0", port=80)
