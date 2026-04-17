from mcp.server.fastmcp import FastMCP
from mcp_server.registry import TASKS
import logging
import psycopg2

# cria servidor MCP
mcp = FastMCP("shopagent-mcp")


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="shopagent",
        user="shopagent",
        password="shopagent"
    )

def normalize_task(task: str) -> str:
    task = task.lower().strip()

    if "business" in task:
        return "business_analysis"

    if "review" in task:
        return "reviews_summary"

    if "overview" in task or "count" in task:
        return "data_overview"

    return task

# -------------------------
# TOOL 1: run_sql
# -------------------------
@mcp.tool()
def run_sql(query: str) -> dict:
    """Execute a SQL query and return results"""

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(query)

    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "columns": columns,
        "rows": rows
    }


# -------------------------
# TOOL 2: get_schema
# -------------------------
@mcp.tool()
def get_schema() -> list:
    """Return database schema"""

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, column_name
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

#---------------
# TOOL 3: get_reviews
#---------------
@mcp.tool()
def sample_reviews(n: int = 100) -> dict:
    """Read and analyze reviews from JSONL file"""

    import json
    from collections import Counter

    file_path = "gen/data/reviews/reviews.jsonl"

    reviews = []
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            reviews.append(json.loads(line))

    sample = reviews[:10]

    # structure
    fields = list(sample[0].keys()) if sample else []

    # distributions
    sentiment_dist = Counter(r.get("sentiment") for r in reviews if "sentiment" in r)
    rating_dist = Counter(r.get("rating") for r in reviews if "rating" in r)

    return {
        "sample_reviews": sample,
        "fields": fields,
        "sentiment_distribution": dict(sentiment_dist),
        "rating_distribution": dict(rating_dist),
    }

#------------
# Tool 3 execute tasks
#------------
@mcp.tool()
def execute_task(task: str) -> dict:
    """Execute a predefined task"""
    task_name = normalize_task(task)

    if task_name not in TASKS:
        return {"error": f"Task {task} not found"}

    return TASKS[task_name]()

# -------------------------
# START SERVER
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


if __name__ == "__main__":
    logging.info("MCP Server is running")
    mcp.run(transport="stdio")