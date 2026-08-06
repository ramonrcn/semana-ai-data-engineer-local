from pathlib import Path

from src.runtime.runtime import AgentRuntime
from src.runtime.registry import CapabilityRegistry
from src.runtime.knowledge.registry import KnowledgeRegistry
from src.runtime.knowledge.selector import BaseKnowledgeSelector
from src.runtime.knowledge.passthrough import  PassthroughKnowledgeSelector
from src.runtime.prompt.base import BasePromptCompiler
from src.runtime.prompt_compiler.compiler import PromptCompiler
from src.runtime.llm.base import BaseLLM
from src.runtime.llm.fake import FakeLLM

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
        or PromptCompiler()
    )

    return AgentRuntime(

        cap_registry,

        kb_registry,

        llm,

        selector,

        prompt_compiler,

    )    