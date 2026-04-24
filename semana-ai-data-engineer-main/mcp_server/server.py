from mcp.server import FastMCP
from mcp_server.orchestrator import run_task
from mcp_server.logging_config import get_logger

logger = get_logger(__name__)

mcp = FastMCP("shopagent-mcp")


@mcp.tool()
def execute_task(task_name: str, kwargs: dict={}):
    logger.info(
        f"[MCP] Tool called: execute_task(task_name={task_name})",
        extra={"trace_id": "entry"}
    )

    result = run_task(task_name, **kwargs)

    if isinstance(result, dict) and "result" in result:
        return result["result"]

    logger.info(
        f"[MCP] Tool completed: {task_name}",
        extra={"trace_id": result.get("trace_id", "unknown")}
    )

if __name__ == "__main__":
    logger.info("🚀 MCP Server starting...", extra={"trace_id": "system"})
    logger.info("🔧 Registered tools: execute_task", extra={"trace_id": "system"})

    mcp.run()