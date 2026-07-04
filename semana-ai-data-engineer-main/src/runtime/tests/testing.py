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
from src.runtime.bootstrap import build_runtime


def build_test_runtime(
    llm: BaseLLM | None = None,
    selector: BaseKnowledgeSelector | None = None,
    prompt_compiler: BasePromptCompiler | None = None,
):
    return build_runtime(
        llm=llm,
        selector=selector,
        prompt_compiler=prompt_compiler,
    )
   