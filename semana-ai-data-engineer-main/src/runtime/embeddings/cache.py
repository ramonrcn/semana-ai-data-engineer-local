import numpy as np


class EmbeddingCache:

    def __init__(self):

        self._cache: dict[str, np.ndarray] = {}

    def get(
        self,
        text: str,
    ):

        return self._cache.get(text)

    def put(
        self,
        text: str,
        embedding,
    ):

        self._cache[text] = embedding

    def contains(
        self,
        text: str,
    ) -> bool:

        return text in self._cache