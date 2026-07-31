from abc import ABC
from abc import abstractmethod

from ..context import RuntimeContext
from .prompt import Prompt


class BasePromptCompiler(ABC):

    @abstractmethod
    def compile(
        self,
        context: RuntimeContext,
    ) -> Prompt:
        ...