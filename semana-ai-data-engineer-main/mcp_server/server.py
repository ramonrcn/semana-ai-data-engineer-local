from mcp.server.fastmcp import FastMCP

from mcp_server.logging_config import get_logger
from mcp_server.orchestrator import run_task

logger = get_logger(__name__)

mcp = FastMCP("shopagent-mcp")


@mcp.tool()
def execute_task(task_name: str) -> dict:
    """
    Main entrypoint for all tasks.
    """

    logger.info(f"[TOOL] execute_task called with: {task_name}")

    return run_task(task_name)


if __name__ == "__main__":
    logger.info("[MCP] Server starting...")
    mcp.run()