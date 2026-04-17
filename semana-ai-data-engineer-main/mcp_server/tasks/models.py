import os
from mcp_server.services.files import read_file
from mcp_server.generators.model_generator import generate_models

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TARGET_PATH = os.path.join(BASE_DIR, "src/day1/models.py")
SQL_PATH = "gen/init.sql"

def get_models():
    path = TARGET_PATH

    # -------------------------
    # 1. CHECK: FILE EXISTS
    # -------------------------
    if os.path.exists(path):
        print("[MCP] models.py já existe — retornando conteúdo")

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "status": "exists",
            "content": content
        }

    # 🚨 IMPORTANTE: TUDO ABAIXO SÓ RODA SE NÃO EXISTIR

    print("[MCP] models.py NÃO existe — gerando arquivo")

    from mcp_server.services.files import read_file
    from mcp_server.generators.model_generator import generate_models

    sql = read_file("gen/init.sql")
    reviews = read_file("gen/shadowtraffic.json")

    code = generate_models(sql, reviews)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(code)

    return {
        "status": "created",
        "content": code
    }