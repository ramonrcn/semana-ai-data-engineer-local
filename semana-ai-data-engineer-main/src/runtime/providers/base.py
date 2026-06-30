from abc import ABC
from abc import abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def invoke(
        self,
        prompt: str
    ) -> str:
        pass