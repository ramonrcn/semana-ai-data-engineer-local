from abc import ABC, abstractmethod

import numpy as np


class BaseSimilarityMetric(ABC):

    @abstractmethod
    def score(
        self,
        query_vector: np.ndarray,
        document_vectors: np.ndarray,
    ) -> np.ndarray:
        """Returns one score for each document."""