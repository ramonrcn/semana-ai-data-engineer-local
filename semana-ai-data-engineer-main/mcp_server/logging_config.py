import logging
import os
from typing import Optional
from datetime import datetime, timezone


#  LOG DIRECTORY INSIDE MCP
LOG_DIR = os.path.join(os.path.dirname(__file__), ".logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "runtime.log")


class TraceFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        trace_id = getattr(record, "trace_id", "no-trace")
        record.trace_id = trace_id
        return super().format(record)

class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def format(self, record: logging.LogRecord) -> str:
        trace_id = getattr(record, "trace_id", "no-trace")
        record.trace_id = trace_id
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = UTCFormatter(
        "[%(asctime)s UTC] [%(levelname)s] [%(name)s] [trace_id=%(trace_id)s] %(message)s"
    )

    #  FILE HANDLER (inside mcp_server/.logs/)
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)

    #  CONSOLE HANDLER
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    logger.info("Logger initialized", extra={"trace_id": "system"})

    return logger


def log_with_trace(logger: logging.Logger, level: str, message: str, trace_id: Optional[str]):
    extra = {"trace_id": trace_id or "no-trace"}

    if level == "info":
        logger.info(message, extra=extra)
    elif level == "warning":
        logger.warning(message, extra=extra)
    elif level == "error":
        logger.error(message, extra=extra)