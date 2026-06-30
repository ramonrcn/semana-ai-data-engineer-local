from anthropic.types.beta import beta_all_thinking_turns_param
from sentence_transformers import SentenceTransformer
from .base import BaseEmbeddingModel
from .cache import EmbeddingCache
import numpy as np

class SentenceTransformerEmbeddingModel(BaseEmbeddingModel):

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):

        self._model_name = model_name
        self._model = SentenceTransformer(model_name)
        self._cache = EmbeddingCache()

    @property
    def dimension(self) -> int:
        return self._model.get_embedding_dimension()

    @property
    def model_name(self) -> str:
        return self._model_name

    def encode(
        self,
        texts: list[str],
    ):

        embeddings = []

        missing = []

        missing_index = []

        hits = 0
        misses = 0

        for i, text in enumerate(texts):

            cached = self._cache.get(text)

            if cached is None:

                misses += 1

                missing.append(text)
                missing_index.append(i)

                embeddings.append(None)

            else:

                hits += 1

                embeddings.append(cached)

        if missing:

            new_embeddings = self._model.encode(

                missing,

                convert_to_numpy=True,

                normalize_embeddings=True,

            )

            for index, text, embedding in zip(
                missing_index,
                missing,
                new_embeddings,
            ):

                self._cache.put(
                    text,
                    embedding,
                )

                embeddings[index] = embedding

        total = hits + misses

        hit_rate = (
            hits / total
            if total
            else 0.0
        )

        print("\n=== EMBEDDING CACHE ===")
        print(f"Hits     : {hits}")
        print(f"Misses   : {misses}")
        print(f"Hit Rate : {hit_rate:.1%}")

        return np.asarray(
            embeddings
        )