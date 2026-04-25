from mcp.server import FastMCP
from mcp_server.orchestrator import run_task
from mcp_server.logging_config import get_logger

logger = get_logger(__name__)

mcp = FastMCP("shopagent-mcp")


@mcp.tool()
def execute_task(task_name: str, **kwargs):
    """
    Entry point for ALL MCP execution.
    """

    # --- FIX: FLATTEN BAD KWARGS FROM CONTINUE ---
    if isinstance(kwargs, dict):
        flat_kwargs = kwargs
    else:
        flat_kwargs = {}


    # --- LOG INPUT ---
    logger.info(
        f"[MCP] Tool called: execute_task(task_name={task_name}, kwargs={flat_kwargs})",
        extra={"trace_id": "entry"}
    )

    # --- EXECUTE ---
    result = run_task(task_name, **kwargs)

    # --- LOG OUTPUT ---
    logger.info(
        f"[MCP] Tool completed: {task_name}",
        extra={"trace_id": result.get("trace_id", "unknown")}
    )

    # --- RETURN CLEAN RESULT ---
    if isinstance(result, dict) and "result" in result:
        return result["result"]

    return result


if __name__ == "__main__":
    logger.info("🚀 MCP Server starting...", extra={"trace_id": "system"})
    logger.info("🔧 Registered tools: execute_task", extra={"trace_id": "system"})

    mcp.run()