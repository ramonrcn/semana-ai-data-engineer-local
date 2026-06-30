from ..embeddings.base import BaseEmbeddingModel
from ..similarity.base import BaseSimilarityMetric
from .vector import VectorKnowledgeSelector


class EmbeddingKnowledgeSelector(VectorKnowledgeSelector):
    """Ranks documents using neural embeddings."""

    def __init__(
        self,
        embedding_model: BaseEmbeddingModel,
        *,
        top_k: int | None = None,
        similarity: BaseSimilarityMetric | None = None,
    ) -> None:

        super().__init__(similarity)

        self._embedding_model = embedding_model
        self._top_k = top_k

    def select(
        self,
        documents,
        objective: str = "",
    ):

        if not documents:
            return []

        corpus = [
            document.content
            for document in documents
        ]

        embeddings = self._embedding_model.encode(
            corpus + [objective]
        )

        document_vectors = embeddings[:-1]

        query_vector = embeddings[-1:].reshape(1, -1)

        print("\n=== EMBEDDINGS ===")

        print(
            f"Model: {self._embedding_model.model_name}"
        )

        print(
            f"Dimension: {self._embedding_model.dimension}"
        )

        return self._rank_documents(
            documents,
            document_vectors,
            query_vector,
        )