from .base import BasePromptCompiler
from ..context import RuntimeContext
from .prompt import Prompt

class MarkdownPromptCompiler(BasePromptCompiler):

    def compile(
        self,
        context: RuntimeContext,
    ) -> Prompt:

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

        return Prompt(
            text="\n".join(prompt_parts)
        )