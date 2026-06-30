from abc import ABC
from abc import abstractmethod

from .models import KnowledgeDocument


class BaseKnowledgeSelector(ABC):

    # Selects which documents will be injected into the prompt.
    @abstractmethod
    def select(
        self,
        documents: list[KnowledgeDocument],
        objective: str
    ) -> list[KnowledgeDocument]:

        ...