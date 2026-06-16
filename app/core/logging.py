import logging
import sys
from typing import Any
import structlog
from structlog.typing import EventDict

from app.core.context import get_correlation_id


def _add_correlation_id(_: Any, __: str, event_dict: EventDict) -> EventDict:
    event_dict["correlation_id"] = get_correlation_id()
    return event_dict


def logging_config() -> None:
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            _add_correlation_id,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.PrintLoggerFactory(),
    )


class Logger:
    _logger = structlog.get_logger()

    @classmethod
    def log(cls, event: str, **kwargs: Any) -> None:
        cls._logger.info(event.upper(), **kwargs)

    @classmethod
    def error(cls, event: str, **kwargs: Any) -> None:
        cls._logger.error(event.upper(), **kwargs)
