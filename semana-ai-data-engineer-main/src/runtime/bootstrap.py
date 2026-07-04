from pathlib import Path

from .runtime import AgentRuntime
from .registry import CapabilityRegistry
from .knowledge.registry import KnowledgeRegistry
from .knowledge.selector import BaseKnowledgeSelector
from .knowledge.passthrough import  PassthroughKnowledgeSelector
from .prompt.base import BasePromptCompiler
from .prompt.markdown import MarkdownPromptCompiler
from .llm.base import BaseLLM
from .llm.fake import FakeLLM

def build_runtime(
    llm: BaseLLM | None = None,
    selector: BaseKnowledgeSelector | None = None,
    prompt_compiler: BasePromptCompiler | None = None,
) -> AgentRuntime:
    """
    Builds a fully configured AgentRuntime with default implementations.
    """

    cap_registry = CapabilityRegistry()
    # cap_registry.load_directory(Path(".claude/agents"))
    project_root = Path(__file__).resolve().parents[2]

    cap_registry.load_directory(
        project_root / ".claude" / "agents"
    )

    print("\nRegistered capabilities:")

    for capability in cap_registry.list():
        print(f" - {capability}")

    kb_registry = KnowledgeRegistry()
    # kb_registry.load_directory(Path(".claude/kb"))
    kb_registry.load_directory(
        project_root / ".claude" / "kb"
    )

    llm = llm or FakeLLM()

    selector = (
        selector
        or PassthroughKnowledgeSelector()
    )

    prompt_compiler = (
        prompt_compiler
        or MarkdownPromptCompiler()
    )

    return AgentRuntime(

        cap_registry,

        kb_registry,

        llm,

        selector,

        prompt_compiler,

    )    