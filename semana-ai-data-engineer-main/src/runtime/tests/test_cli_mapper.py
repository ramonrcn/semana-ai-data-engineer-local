from src.runtime.integrations.cli.request_mapper import (
    CLIRequestMapper,
)


mapper = CLIRequestMapper()

request = mapper.map(
    "Create Pydantic models"
)

print(request)