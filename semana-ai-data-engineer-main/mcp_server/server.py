from mcp.server.fastmcp import FastMCP
from mcp_server.orchestrator import run_task

mcp = FastMCP("test-mcp")


def execute_task(task_name: str, **kwargs):
    return run_task(task_name, **kwargs)


mcp.add_tool(execute_task)


if __name__ == "__main__":
    mcp.run()