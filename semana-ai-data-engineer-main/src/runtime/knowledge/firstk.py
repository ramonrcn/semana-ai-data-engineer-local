from .selector import BaseKnowledgeSelector


class FirstKKnowledgeSelector(
    BaseKnowledgeSelector
):

    def __init__(
        self,
        k: int
    ):

        if k <= 0:
            raise ValueError(
                "k must be greater than zero."
            )

        self.k = k

    def select(
        self,
        documents,
        objective: str = ""
    ):

        return documents[: self.k]