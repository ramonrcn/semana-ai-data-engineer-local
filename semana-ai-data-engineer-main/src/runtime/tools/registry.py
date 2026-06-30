from .models import Tool


class ToolRegistry:

    def __init__(self):

        self._tools = {}

    def register(
        self,
        tool: Tool
    ):

        self._tools[
            tool.name
        ] = tool

    def get(
        self,
        tool_name: str
    ) -> Tool:

        return self._tools[
            tool_name
        ]

    def list_tools(
        self
    ):

        return sorted(
            self._tools.keys()
        )