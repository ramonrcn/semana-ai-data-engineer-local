from sentence_transformers import SentenceTransformer
from .base import BaseEmbeddingModel
import numpy as np

class SentenceTransformerEmbeddingModel(BaseEmbeddingModel):

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):

        self._model_name = model_name
        self._model = SentenceTransformer(model_name)

    @property
    def dimension(self) -> int:
        return self._model.get_embedding_dimension()

    @property
    def model_name(self) -> str:
        return self._model_name

    def encode(
        self,
        texts: list[str],
    ) -> np.ndarray:

        return self._model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )