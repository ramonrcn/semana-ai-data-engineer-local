from pathlib import Path

from .registry import (
    CapabilityRegistry
)

registry = (
    CapabilityRegistry()
)

registry.load_directory(
    Path(".claude/agents")
)

capability = registry.get(
    "domain.shopagent-builder"
)

print()

print(
    capability.name
)

print()

for tool in capability.tools:

    print(tool)