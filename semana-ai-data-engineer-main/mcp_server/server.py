
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-mcp")

def ping():
    return {"status": "ok"}

mcp.add_tool(ping)

if __name__ == "__main__":
    mcp.run()