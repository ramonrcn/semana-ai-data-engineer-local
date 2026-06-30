from .models import Tool
from .registry import ToolRegistry

registry = ToolRegistry()

registry.register(
    Tool(
        name="generate_models",
        description=
        "Generate Pydantic models"
    )
)

print(
    registry.list_tools()
)