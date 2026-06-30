from abc import ABC, abstractmethod

import numpy as np


class BaseEmbeddingModel(ABC):

    @abstractmethod
    def encode(
        self,
        texts: list[str],
    ) -> np.ndarray:
        """Returns one embedding per text."""