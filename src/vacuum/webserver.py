from asyncio import AbstractEventLoop, get_event_loop, Task
from dataclasses import asdict
from datetime import datetime
from typing import Tuple

from quart import Quart, request

from .logger import get_logger, set_quart_logger_formatter
from .streamer import stream
from .state import state

logger = get_logger(__name__)
app = Quart(__name__)
set_quart_logger_formatter()


STREAMING_TASK_NAME: str = "streaming"


def form_response(fields: dict = {}, success: bool = True) -> dict:
    return {
        **asdict(state),
        **{
            "server_time": datetime.now(),
            "success": success,
            "path": request.path,
            "method": request.method,
            "status": "200 OK",
            "status_code": 200,
        },
        **fields,
    }


@app.route("/healthz", methods=["GET"])
async def healthz() -> Tuple[str, int]:
    return "", 200


@app.route("/status", methods=["GET"])
async def status() -> dict:
    return form_response()


@app.route("/start", methods=["POST"])
async def start() -> dict:
    logger.info("starting")

    if not state.streaming:
        loop: AbstractEventLoop = get_event_loop()
        loop.create_task(stream(), name=STREAMING_TASK_NAME)
        state.streaming = True

    return form_response()


@app.route("/stop", methods=["POST"])
async def stop() -> dict:
    logger.info("stopping")

    if state.streaming:
        for task in Task.all_tasks():
            if task.get_name() == STREAMING_TASK_NAME:
                task.cancel()

        state.streaming = False

    return form_response()


def error(code: int, status: str) -> Tuple[dict, int]:
    return (
        {
            "server_time": datetime.now(),
            "success": False,
            "path": request.path,
            "method": request.method,
            "status": f"{code} {status}",
            "status_code": code,
        },
        code,
    )


@app.errorhandler(404)
async def page_not_found(e) -> Tuple[dict, int]:
    return error(404, "Not Found")


@app.errorhandler(405)
async def method_not_allowed(e) -> Tuple[dict, int]:
    return error(405, "Method Not Allowed")


def webserver() -> None:
    app.run(host="0.0.0.0", port=80)
