import os
from mcp_server.services.files import read_file
from mcp_server.generators.model_generator import generate_models

<<<<<<< Updated upstream
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TARGET_PATH = os.path.join(BASE_DIR, "src/day1/models.py")
SQL_PATH = "gen/init.sql"
=======
BASE_DIR = Path(__file__).resolve().parents[2]
SQL_PATH = BASE_DIR / "gen" / "init.sql"
SHADOW_PATH = BASE_DIR / "gen" / "shadowtraffic.json"
>>>>>>> Stashed changes

def get_models(**kwargs):
    sql = read_file(SQL_PATH)
    shadow = read_file(SHADOW_PATH)

    return generate_models(sql, shadow)