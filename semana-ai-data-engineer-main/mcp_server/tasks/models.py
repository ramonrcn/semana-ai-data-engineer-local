import os
from pathlib import Path
from mcp_server.services.files import read_file
from mcp_server.generators.model_generator import generate_models

BASE_DIR = Path(__file__).resolve().parents[2]
SQL_PATH = BASE_DIR / "gen" / "init.sql"

def get_models(**kwargs):
    from mcp_server.services.files import read_file

    sql = read_file(SQL_PATH)

    return generate_models(sql)