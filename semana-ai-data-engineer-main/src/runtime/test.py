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

print()

for capability_id in registry.list():

    print(
        capability_id
    )

print()

capability = registry.get(
    "domain.shopagent-builder"
)

print(
    capability.extract_kb_refs()
)
print('#Tools')
print(capability.tools)