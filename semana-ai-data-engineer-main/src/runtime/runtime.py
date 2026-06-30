from .registry import CapabilityRegistry
from .knowledge.registry import KnowledgeRegistry
from .knowledge.selector import BaseKnowledgeSelector
from .knowledge.passthrough import (
    PassthroughKnowledgeSelector
)
from .context import RuntimeContext


class AgentRuntime:

    def __init__(
        self,
        capability_registry: CapabilityRegistry,
        knowledge_registry: KnowledgeRegistry,
        llm,
        knowledge_selector: (
            BaseKnowledgeSelector | None
        ) = None
    ):

        self.capabilities = capability_registry

        self.knowledge = knowledge_registry

        self.llm = llm

        # Strategy responsible for selecting which KBs enter the prompt.
        self.knowledge_selector = (
            knowledge_selector
            or PassthroughKnowledgeSelector()
        )

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

        return RuntimeContext(

            capability=capability,

            knowledge=documents,

            environment_tools=(
                capability.required_environment_tools()
            )

        )

    def assemble_prompt(
        self,
        capability_id: str,
        objective: str
    ) -> str:

        context = self.build_context(
            capability_id,
            objective
        )

        prompt_parts = []

        prompt_parts.append(
            "# AGENT\n"
        )

        prompt_parts.append(
            context.capability.prompt
        )

        prompt_parts.append(
            "\n\n# KNOWLEDGE\n"
        )

        for document in context.knowledge:

            prompt_parts.append(
                f"\n## {document.id}\n"
            )

            prompt_parts.append(
                document.content
            )

        prompt_parts.append(
            "\n\n# OBJECTIVE\n"
        )

        prompt_parts.append(
            objective
        )

        return "\n".join(
            prompt_parts
        )

    def run(
        self,
        capability_id: str,
        objective: str
    ):

        prompt = self.assemble_prompt(
            capability_id,
            objective
        )

        return self.llm.invoke(
            prompt
        )