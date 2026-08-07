from .registry import CapabilityRegistry
from .knowledge.registry import KnowledgeRegistry
from .knowledge.selector import BaseKnowledgeSelector
from .context import RuntimeContext
from .tracing.trace import RuntimeTrace
from .tracing.printer import TracePrinter
from .tracing.span import TraceSpan
from .prompt.base import BasePromptCompiler
from .knowledge.retrieved import RetrievedKnowledge
from src.runtime.prompt.prompt import Prompt


class AgentRuntime:

    def __init__(
        self,
        capability_registry: CapabilityRegistry,
        knowledge_registry: KnowledgeRegistry,
        llm,
        knowledge_selector: BaseKnowledgeSelector,
        prompt_compiler: BasePromptCompiler,
    ):

        self.capabilities = capability_registry

        self.knowledge = knowledge_registry

        self.llm = llm

        # Strategy responsible for selecting which KBs enter the prompt.
        self.knowledge_selector = knowledge_selector

        self.prompt_compiler = prompt_compiler

    def build_context(
        self,
        capability_id: str,
        objective: str = ""
    ) -> RuntimeContext:

        capability = self.capabilities.get(
            capability_id
        )

        documents = self.knowledge.resolve(
            capability.required_knowledge()
        )

        # Delegates document selection to the configured strategy.
        documents = (
            self.knowledge_selector.select(
                documents,
                objective
            )
        )

        retrieved = [
            RetrievedKnowledge(
                document=document,
            )

            for document in documents
        ]

        return RuntimeContext(

            capability=capability,

            objective=objective,

            knowledge=retrieved,

            environment_tools=(
                capability.required_environment_tools()
            )

        )

    def assemble_prompt(
        self,
            context: RuntimeContext,
        ) -> Prompt:

            return self.prompt_compiler.compile(
                context
            )

    def run(
        self,
        capability_id: str,
        objective: str,
    ):
        trace = RuntimeTrace.start()

        trace.capability = capability_id
        trace.objective = objective

        trace.knowledge_selector = (
            self.knowledge_selector.__class__.__name__
        )

        trace.llm = self.llm.__class__.__name__
                
        with trace.span(
            "knowledge_selection",
            selector=trace.knowledge_selector,
        ) as event:

            context = self.build_context(
                capability_id,
                objective,
            )

            trace.knowledge_documents = len(
                context.knowledge
            )

            event.add(
                documents=len(
                    context.knowledge
                )
            )

        with trace.span(
            "prompt_assembly",
        ) as event:

            prompt = self.assemble_prompt(
                context,
            )

            trace.prompt_size = len(
                prompt.text
            )

            event.add(
                prompt_size=len(
                    prompt.text
                )
            )
        
        with trace.span(
            "llm_invocation",
            provider=trace.llm,
        ):

            response = self.llm.invoke(
                prompt
            )

        trace.finish()

        TracePrinter.print(trace)

        return response