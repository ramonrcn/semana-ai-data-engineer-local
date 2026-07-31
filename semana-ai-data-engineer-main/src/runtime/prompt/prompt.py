from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Prompt:
    """
    Canonical Runtime prompt.

    This object represents the final prompt produced by the Runtime,
    independent of any LLM provider.
    """

    text: str

    def __str__(self) -> str:
        return self.text