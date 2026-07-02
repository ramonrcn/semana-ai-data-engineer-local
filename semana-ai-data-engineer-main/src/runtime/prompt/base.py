from abc import ABC
from abc import abstractmethod

from ..context import RuntimeContext


class BasePromptCompiler(ABC):

    @abstractmethod
    def compile(
        self,
        context: RuntimeContext,
    ) -> str:
        ...