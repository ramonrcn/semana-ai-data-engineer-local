from .base import (
    LLMProvider
)


class MockLLM(
    LLMProvider
):

    def invoke(
        self,
        prompt: str
    ) -> str:

        return (
            f"Prompt received with "
            f"{len(prompt)} chars"
        )