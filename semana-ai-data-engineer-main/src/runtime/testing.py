from pathlib import Path
from .registry import CapabilityRegistry
from .runtime import AgentRuntime
from .knowledge.registry import KnowledgeRegistry
from .knowledge.selector import BaseKnowledgeSelector
from .knowledge.passthrough import  PassthroughKnowledgeSelector
from .llm.base import BaseLLM
from .llm.fake import FakeLLM


def build_test_runtime(
    llm: BaseLLM | None = None,
    selector: BaseKnowledgeSelector | None = None,
):

    cap_registry = CapabilityRegistry()
    cap_registry.load_directory(Path(".claude/agents"))

    kb_registry = KnowledgeRegistry()
    kb_registry.load_directory(Path(".claude/kb"))

    llm = llm or FakeLLM()

    selector = (
        selector
        or PassthroughKnowledgeSelector()
    )

    return AgentRuntime(

        cap_registry,

        kb_registry,

        llm,

        selector,

    )