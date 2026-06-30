from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

from .models import KnowledgeDocument
from .vector import VectorKnowledgeSelector
from ..similarity.base import BaseSimilarityMetric


class LSAKnowledgeSelector(VectorKnowledgeSelector):
    """Ranks documents using Latent Semantic Analysis."""

    def __init__(
        self,
        *,
        top_k: int | None = None,
        n_components: int = 100,
        similarity: BaseSimilarityMetric | None = None,
    ) -> None:

        super().__init__(similarity)

        self._top_k = top_k
        self._n_components = n_components

    def select(
        self,
        documents,
        objective="",
    ):

        if not documents:
            return []

        corpus = [
            document.content
            for document in documents
        ]

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        tfidf = vectorizer.fit_transform(
            corpus + [objective]
        )

        max_components = min(
            self._n_components,
            tfidf.shape[0] - 1,
            tfidf.shape[1] - 1,
        )

        if max_components <= 0:
            return documents

        svd = TruncatedSVD(
            n_components=max_components,
            random_state=42,
        )

        latent_space = svd.fit_transform(tfidf)

        document_vectors = latent_space[:-1]

        objective_vector = latent_space[-1].reshape(1, -1)

        # Diagnóstico específico do algoritmo.
        print("\n=== LSA ===")

        print(
            f"Components: {max_components}"
        )

        print(
            f"Explained Variance: "
            f"{svd.explained_variance_ratio_.sum():.3f}"
        )

        return self._rank_documents(
            documents,
            document_vectors,
            objective_vector,
        )