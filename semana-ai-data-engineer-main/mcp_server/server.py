from mcp.server.fastmcp import FastMCP
from mcp_server.orchestrator import run_task
from mcp_server.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("shopagent-mcp")

@mcp.tool()
def execute_task(task_name: str) -> dict:
    import logging

    logging.info(f"[TOOL] execute_task called with: {task_name}")

    if not isinstance(task_name, str):
        return {
            "status": "error",
            "message": "task_name must be a string"
        }

    try:
        result = run_task(task_name)

        logging.info(f"[TOOL] success: {task_name}")

        return result

    except Exception as e:
        logging.error(f"[TOOL] error: {str(e)}")

        return {
            "status": "error",
            "message": str(e)
        }

# if __name__ == "__main__":
#     logger.info("MCP Server is running")
#     mcp.run(transport="stdio")

if __name__ == "__main__":
    logger.info("🚀 MCP Server starting (STDIO mode)")

    try:
        mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"[FATAL] MCP crashed: {e}")