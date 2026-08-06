from abc import ABC, abstractmethod
from src.runtime.prompt.prompt import Prompt


class BaseLLM(ABC):

    @abstractmethod
    def invoke(
        self,
        prompt: Prompt
    ) -> str:
        pass