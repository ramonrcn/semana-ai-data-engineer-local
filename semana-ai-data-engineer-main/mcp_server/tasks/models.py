import os
from mcp_server.services.files import read_file
from mcp_server.generators.model_generator import generate_models

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TARGET_PATH = os.path.join(BASE_DIR, "src/day1/models.py")
SQL_PATH = "gen/init.sql"

def get_models(**kwargs):
    from mcp_server.services.files import read_file

    sql = read_file(SQL_PATH)

    return generate_models(sql)