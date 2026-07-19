from src.runtime.context import RuntimeContext


_EXECUTION_RULES = """
            ---

            # EXECUTION RULES

            You MUST answer using ONLY the reference knowledge provided below.

            If the answer cannot be derived from the provided knowledge,
            explicitly say so instead of inventing information.

            Always prefer the provided documentation over assumptions.

            Do not ignore the reference knowledge.

            """


class PromptCompiler:
    """Compiles a RuntimeContext into a deterministic prompt."""

    def compile(
        self,
        runtime_context: RuntimeContext,
    ) -> str:

        prompt_parts: list[str] = []

        prompt_parts.extend(
            self._build_system(runtime_context)
        )

        prompt_parts.extend(
            self._build_execution_rules()
        )

        prompt_parts.extend(
            self._build_objective(runtime_context)
        )

        prompt_parts.extend(
            self._build_reference_knowledge(runtime_context)
        )

        return "\n".join(prompt_parts)

    def _build_system(
        self,
        runtime_context: RuntimeContext,
    ) -> list[str]:

        return [
            "# SYSTEM\n",
            runtime_context.capability.prompt,
        ]

    def _build_execution_rules(self) -> list[str]:

        return [_EXECUTION_RULES]

    def _build_objective(
        self,
        runtime_context: RuntimeContext,
    ) -> list[str]:

        if not runtime_context.objective:
            return []

        return [
            "\n\n# OBJECTIVE\n",
            runtime_context.objective,
        ]

    def _build_reference_knowledge(
        self,
        runtime_context: RuntimeContext,
    ) -> list[str]:

        if not runtime_context.knowledge:
            return []

        prompt_parts = [
            "\n\n# REFERENCE KNOWLEDGE\n"
        ]

        for knowledge in runtime_context.knowledge:
            prompt_parts.append(
                f"\n## {knowledge.document.id}\n"
            )

            prompt_parts.append(
                knowledge.document.content
            )

        return prompt_parts