from .base import BasePromptCompiler
from ..context import RuntimeContext


class MarkdownPromptCompiler(BasePromptCompiler):

    def compile(
        self,
        context: RuntimeContext,
    ) -> str:

        prompt_parts = []

        # =====================================================================
        # SYSTEM
        # =====================================================================

        prompt_parts.append(
            "# SYSTEM\n"
        )

        prompt_parts.append(
            context.capability.prompt
        )

        prompt_parts.append(
            """
            ---

            # EXECUTION RULES

            You MUST answer using ONLY the reference knowledge provided below.

            If the answer cannot be derived from the provided knowledge,
            explicitly say so instead of inventing information.

            Always prefer the provided documentation over assumptions.

            Do not ignore the reference knowledge.

            """
        )
                    
        # =====================================================================
        # OBJECTIVE
        # =====================================================================

        prompt_parts.append(
            "\n\n# OBJECTIVE\n"
        )

        prompt_parts.append(
            context.objective
        )

        # =====================================================================
        # REFERENCE KNOWLEDGE
        # =====================================================================

        prompt_parts.append(
            "\n\n# REFERENCE KNOWLEDGE\n"
        )

        for knowledge in context.knowledge:

            prompt_parts.append(
                f"\n## {knowledge.document.id}\n"
            )

            prompt_parts.append(
                knowledge.document.content
            )

        return "\n".join(
            prompt_parts
        )