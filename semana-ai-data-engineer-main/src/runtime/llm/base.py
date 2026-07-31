from abc import ABC, abstractmethod
from src.runtime.prompt import Prompt


class BaseLLM(ABC):

    @abstractmethod
    def invoke(
        self,
        prompt: Prompt
    ) -> str:
        pass