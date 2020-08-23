from asyncio import AbstractEventLoop, Task, get_event_loop
from dataclasses import asdict
from datetime import datetime
from functools import wraps
from typing import Callable, Optional, Tuple

from quart import Quart, request
from werkzeug.exceptions import HTTPException

from .config import config
from .logger import get_logger, set_quart_logger_formatter
from .postgres import POSTGRES_HEALTHCHECK_TASK_NAME, postgres_healthcheck
from .state import state
from .streamer import STREAMING_TASK_NAME, stream

logger = get_logger(__name__)
app = Quart(__name__)
set_quart_logger_formatter()


def response(func: Callable) -> Callable:
    @wraps(func)
    async def inner(*args, **kwargs) -> dict:
        extra: Optional[dict] = await func(*args, **kwargs)

        if not extra:
            extra = {"success": True}

        return {
            **asdict(state),
            **{
                "server_time": datetime.now(),
                "path": request.path,
                "method": request.method,
                "status": "200 OK",
                "status_code": 200,
            },
            **extra,
        }

    return inner


def error(code: int, status: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def inner(*args, **kwargs) -> Tuple[dict, int]:
            extra: Optional[dict] = await func(*args, **kwargs)

            if not extra:
                extra = {}

            return (
                {
                    **{
                        "server_time": datetime.now(),
                        "success": False,
                        "path": request.path,
                        "method": request.method,
                        "status": f"{code} {status}",
                        "status_code": code,
                    },
                    **extra,
                },
                code,
            )

        return inner

    return wrapper


@app.route("/healthz", methods=["GET"])
async def healthz() -> Tuple[str, int]:
    return "", 200


@app.route("/status", methods=["GET"])
@response
async def status() -> None:
    pass


@app.route("/start", methods=["POST"])
@response
async def start() -> dict:
    logger.info("starting")

    if state.streaming:
        return {"success": True, "message": "Currently streaming"}

    if not state.postgres:
        return {"success": False, "message": "Postgres not available"}

    loop: AbstractEventLoop = get_event_loop()
    loop.create_task(stream(), name=STREAMING_TASK_NAME)
    state.streaming = True

    return {"success": True, "message": "Started streaming"}


@app.route("/stop", methods=["POST"])
@response
async def stop() -> dict:
    logger.info("stopping")

    if not state.streaming:
        return {"success": True, "message": "Not currently streaming"}

    for task in Task.all_tasks():
        if task.get_name() == STREAMING_TASK_NAME:
            task.cancel()

    state.streaming = False

    return {"success": True, "message": "Stopped streaming"}


@app.errorhandler(404)
@error(404, "Not Found")
async def page_not_found(e: HTTPException) -> None:
    pass


@app.errorhandler(405)
@error(405, "Method Not Allowed")
async def method_not_allowed(e: HTTPException) -> None:
    pass


@app.before_serving
async def startup() -> None:
    loop: AbstractEventLoop = get_event_loop()
    loop.create_task(postgres_healthcheck(), name=POSTGRES_HEALTHCHECK_TASK_NAME)


def webserver() -> None:
    app.run(host=config["webserver"]["host"], port=config["webserver"]["port"])
