import logging
import os

LOG_FILE = os.path.abspath("mcp_server_runtime.log")


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    # 🔥 FILE HANDLER (PRIMARY)
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = False

    logger.info(f"[LOGGER INIT] Writing logs to: {LOG_FILE}")

    return logger
# import logging
# import sys


# def get_logger(name: str) -> logging.Logger:
#     logger = logging.getLogger(name)

#     if logger.handlers:
#         return logger

#     logger.setLevel(logging.INFO)

#     handler = logging.StreamHandler(sys.stdout)

#     formatter = logging.Formatter(
#         "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
#     )

#     handler.setFormatter(formatter)

#     # 🔥 CRITICAL: force flush every log
#     handler.flush = sys.stdout.flush

#     logger.addHandler(handler)
#     logger.propagate = False

#     return logger