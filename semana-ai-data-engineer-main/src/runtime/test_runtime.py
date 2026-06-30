from pathlib import Path

from .registry import (
    CapabilityRegistry
)

from .knowledge.registry import (
    KnowledgeRegistry
)

from .runtime import (
    AgentRuntime
)

cap_registry = (
    CapabilityRegistry()
)

cap_registry.load_directory(
    Path(".claude/agents")
)

kb_registry = (
    KnowledgeRegistry()
)

kb_registry.load_directory(
    Path(".claude/kb")
)

runtime = AgentRuntime(
    cap_registry,
    kb_registry
)

context = runtime.build_context(
    "domain.shopagent-builder"
)

print(
    context["capability"].name
)

print(
    len(
        context["documents"]
    )
)