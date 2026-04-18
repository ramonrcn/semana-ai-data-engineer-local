from mcp.server.fastmcp import FastMCP
from mcp_server.orchestrator import run_task
from mcp_server.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("shopagent-mcp")


@mcp.tool()
def execute_task(task_name: str, content: str = "") -> dict:
    """
    Execute a predefined task via MCP
    """
    logger.info("[MCP] execute_task", extra={"task_name": task_name})
    return run_task(task_name, content)


if __name__ == "__main__":
    logger.info("MCP Server is running")
    mcp.run(transport="stdio")