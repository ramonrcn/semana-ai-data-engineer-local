import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from .base import BaseSimilarityMetric


class CosineSimilarityMetric(BaseSimilarityMetric):

    def score(
        self,
        query_vector,
        document_vectors,
    ) -> np.ndarray:

        return cosine_similarity(
            query_vector,
            document_vectors,
        ).ravel()