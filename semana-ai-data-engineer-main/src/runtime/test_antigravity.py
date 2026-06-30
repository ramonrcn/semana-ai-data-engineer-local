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

from .builders.agent_builder import (
    AgentBuilder
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
    kb_registry,
    llm=None
)

builder = AgentBuilder(
    runtime
)

config = builder.build_config(
    "domain.shopagent-builder"
)

print()

print(type(config))

print()

print(config.capability_id)

print()

print(
    len(
        config.system_instructions
    )
)

print()

print(
    config.system_instructions[:1000]
)