from pathlib import Path
from src.runtime.registry import CapabilityRegistry
from src.runtime.runtime import AgentRuntime
from src.runtime.knowledge.registry import KnowledgeRegistry
from src.runtime.knowledge.selector import BaseKnowledgeSelector
from src.runtime.knowledge.passthrough import  PassthroughKnowledgeSelector
from src.runtime.prompt.base import BasePromptCompiler
from src.runtime.prompt.markdown import MarkdownPromptCompiler
from src.runtime.llm.base import BaseLLM
from src.runtime.llm.fake import FakeLLM


def build_test_runtime(
    llm: BaseLLM | None = None,
    selector: BaseKnowledgeSelector | None = None,
    prompt_compiler: BasePromptCompiler | None = None,
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