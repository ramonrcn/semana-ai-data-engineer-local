from .base import BasePromptCompiler
from ..context import RuntimeContext


class MarkdownPromptCompiler(BasePromptCompiler):

    def compile(
        self,
        context: RuntimeContext,
    ) -> str:

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
            context.objective
        )

        return "\n".join(
            prompt_parts
        )