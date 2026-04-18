import os
import logging
from mcp_server.services.files import read_file
from mcp_server.generators.model_generator import generate_models

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TARGET_PATH = os.path.join(BASE_DIR, "src/day1/models.py")
SQL_PATH = "gen/init.sql"


def get_models():
    path = TARGET_PATH

    # -------------------------
    # 1. CHECK: FILE EXISTS
    # -------------------------
    if os.path.exists(path):
        logger.info("[MCP] models.py already exists — returning content")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "status": "exists",
            "content": content,
        }

    # -------------------------
    # 2. GENERATE FILE
    # -------------------------
    logger.info("[MCP] models.py does not exist — generating file")

    sql = read_file("gen/init.sql")
    reviews = read_file("gen/shadowtraffic.json")

    code = generate_models(sql, reviews)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    logger.info("[MCP] models.py created successfully")

    return {
        "status": "created",
        "content": code,
    }