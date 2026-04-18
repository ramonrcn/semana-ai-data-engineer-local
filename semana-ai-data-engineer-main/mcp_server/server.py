import asyncio
from mcp.server.fastmcp import FastMCP

print("🔥🔥🔥 MCP SERVER FILE LOADED 🔥🔥🔥")

mcp = FastMCP("shopagent-mcp")


def execute_task(task_name: str, **kwargs) -> dict:
    print("====================================")
    print(f"[CALL] execute_task → {task_name}")
    print(f"[CALL] kwargs → {kwargs}")

    return {
        "status": "success",
        "task": task_name,
        "debug": "MCP WAS CALLED"
    }


mcp.add_tool(execute_task)


async def _log_tools():
    tools = await mcp.list_tools()
    print("[TOOLS REGISTERED]")
    for tool in tools:
        name = getattr(tool, "name", None) or tool.get("name", "unknown")
        print(f" - {name}")


def main():
    print("🚀 MCP STARTING")

    asyncio.run(_log_tools())

    print("🟢 MCP READY")

    mcp.run()


if __name__ == "__main__":
    main()

# import asyncio
# from mcp.server.fastmcp import FastMCP
# from mcp_server.logging_config import get_logger

# logger = get_logger(__name__)

# mcp = FastMCP("shopagent-mcp")


# def execute_task(task_name: str, **kwargs) -> dict:
#     logger.info(f"[SERVER] execute_task CALLED → task_name={task_name}")
#     logger.info(f"[SERVER] kwargs → {kwargs}")

#     from mcp_server.orchestrator import run_task

#     try:
#         result = run_task(task_name, **kwargs)

#         logger.info(f"[SERVER] execute_task SUCCESS → task_name={task_name}")

#         return result

#     except Exception as e:
#         logger.exception(f"[SERVER] execute_task FAILED → task_name={task_name}")
#         raise e


# # 🔥 FORCE REGISTRATION
# mcp.add_tool(execute_task)


# async def _log_registered_tools():
#     try:
#         tools = await mcp.list_tools()

#         logger.info("🔍 [MCP] Registered tools:")

#         for tool in tools:
#             name = getattr(tool, "name", None) or tool.get("name", "unknown")
#             logger.info(f"   - {name}")

#     except Exception:
#         logger.exception("[MCP] Failed to inspect tool registry")


# def main():
#     logger.info("🚀 MCP Server starting...")

#     asyncio.run(_log_registered_tools())

#     logger.info("🟢 MCP Server READY — waiting for tool calls...")

#     # 🔥 THIS IS IMPORTANT: run with stdio (better for real-time logs)
#     mcp.run()


# if __name__ == "__main__":
#     main()