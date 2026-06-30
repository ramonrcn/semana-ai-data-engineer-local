from src.runtime.testing import build_test_runtime
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

from .llm.fake import (
    FakeLLM
)

from .llm.ollama import (
    OllamaLLM
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

runtime = build_test_runtime()
runtime.llm = OllamaLLM()

response = runtime.run(
    "domain.shopagent-builder",
    "Create Pydantic models for ShopAgent"
)

print(response)