from pathlib import Path

from src.runtime.registry import (
    CapabilityRegistry
)

from src.runtime.knowledge.registry import (
    KnowledgeRegistry
)

from src.runtime.runtime import (
    AgentRuntime
)

from src.runtime.builders.agent_builder import (
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