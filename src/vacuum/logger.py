import logging

from pythonjsonlogger.jsonlogger import JsonFormatter

from logging import Logger, getLogger, StreamHandler
from quart.logging import default_handler, serving_handler


def get_formatter() -> JsonFormatter:
    return JsonFormatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s")


def get_logger(name: str, level=logging.INFO) -> Logger:
    logger: Logger = getLogger(name)
    handler: StreamHandler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(get_formatter())
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


def set_quart_logger_formatter() -> None:
    default_handler.setFormatter(get_formatter())
    serving_handler.setFormatter(get_formatter())
