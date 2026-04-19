from mcp.server.fastmcp import FastMCP
from mcp_server.orchestrator import run_task
from mcp_server.logging_config import get_logger

logger = get_logger(__name__)

mcp = FastMCP("test-mcp")


def execute_task(task_name: str, **kwargs):
    logger.info(
        f"[MCP] Tool called: execute_task(task_name={task_name})",
        extra={"trace_id": "entry"}
    )

    result = run_task(task_name, **kwargs)

    logger.info(
        f"[MCP] Tool completed: {task_name}",
        extra={"trace_id": result.get("trace_id", "unknown")}
    )

    return result


mcp.add_tool(execute_task)


if __name__ == "__main__":
    logger.info("🚀 MCP Server starting...", extra={"trace_id": "system"})
    logger.info("🔧 Registered tools: execute_task", extra={"trace_id": "system"})

    mcp.run()