from mcp.server.fastmcp import FastMCP
from mcp_server.orchestrator import run_task
from mcp_server.services.db import get_connection
from mcp_server.logging_config import setup_logging
import logging

# -------------------------
# Setup logging (entrypoint)
# -------------------------
setup_logging()
logger = logging.getLogger(__name__)

# -------------------------
# MCP Server
# -------------------------
mcp = FastMCP("shopagent-mcp")


# -------------------------
# Main tool
# -------------------------
@mcp.tool()
def execute_task(task_name: str, content: str = "") -> dict:
    return run_task(task_name, content)


# -------------------------
# TOOL 1: run_sql
# -------------------------
@mcp.tool()
def run_sql(query: str) -> dict:
    """Execute a SQL query safely"""

    try:
        conn = get_connection()
        cur = conn.cursor()

        # -------------------------
        # Basic safety checks
        # -------------------------
        forbidden = ["insert", "update", "delete", "drop", "alter"]
        if any(f in query.lower() for f in forbidden):
            logger.warning("[SQL] Forbidden operation")
            return {"status": "error", "message": "Write operations not allowed"}

        # -------------------------
        # Execution
        # -------------------------
        cur.execute(query)

        if cur.description:
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
        else:
            columns, rows = [], []

        cur.close()
        conn.close()

        logger.info("[SQL] Query executed", extra={"rows": len(rows)})

        return {
            "status": "success",
            "columns": columns,
            "rows": rows,
        }

    except Exception as e:
        logger.error("[SQL ERROR]", extra={"error": str(e)})
        return {
            "status": "error",
            "message": str(e),
        }


# -------------------------
# TOOL 2: get_schema
# -------------------------
@mcp.tool()
def get_schema() -> dict:
    """Return structured database schema"""

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, column_name
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    schema = {}

    for table, column, dtype in rows:
        if table not in schema:
            schema[table] = {"columns": []}

        schema[table]["columns"].append({
            "name": column,
            "type": dtype
        })

    return schema


# -------------------------
# START SERVER
# -------------------------
if __name__ == "__main__":
    logger.info("MCP Server is running")
    mcp.run(transport="stdio")