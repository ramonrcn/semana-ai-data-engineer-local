from abc import ABC, abstractmethod

import numpy as np


class BaseEmbeddingModel(ABC):

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Embedding dimension."""
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Embedding model identifier."""

    @abstractmethod
    def encode(
        self,
        texts: list[str],
    ) -> np.ndarray:
        """Returns one embedding per input text."""