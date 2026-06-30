from anthropic.types.beta import beta_managed_agents_agent_tool_config_params
from .selector import BaseKnowledgeSelector
from ..similarity.base import BaseSimilarityMetric
from ..similarity.cosine import CosineSimilarityMetric


class VectorKnowledgeSelector(BaseKnowledgeSelector):

    def __init__(
        self,
        similarity: BaseSimilarityMetric | None = None,
    ) -> None:

        self.similarity = (
            similarity
            or CosineSimilarityMetric()
        )

    @property
    def algorithm_name(self) -> str:
        return self.__class__.__name__.replace(
            "KnowledgeSelector",
            ""
        )

    def _rank_documents(
        self,
        documents,
        document_vectors,
        query_vector,
    ):

        scores = self.similarity.score(
            query_vector,
            document_vectors,
        )

        ranked_documents = sorted(
            zip(documents, scores),
            key=lambda item: item[1],
            reverse=True,
        )

        self._print_scores(
            ranked_documents
        )

        selected = [
            document
            for document, _ in ranked_documents
        ]

        if self._top_k is not None:
            selected = selected[: self._top_k]

        return selected

    def _print_scores(
        self,
        ranked_documents,
    ) -> None:

        print(
            f"\n=== {self.algorithm_name.upper()} SCORES ==="
        )

        for document, score in ranked_documents:

            print(
                f"{score:.4f} | {document.id}"
            )