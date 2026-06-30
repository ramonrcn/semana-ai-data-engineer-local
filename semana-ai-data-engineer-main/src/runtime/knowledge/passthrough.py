from .models import KnowledgeDocument
from .selector import BaseKnowledgeSelector


class PassthroughKnowledgeSelector(
    BaseKnowledgeSelector
):

    # Returns every document without filtering.
    def select(
        self,
        documents: list[KnowledgeDocument],
        objective: str
    ) -> list[KnowledgeDocument]:

        return documents