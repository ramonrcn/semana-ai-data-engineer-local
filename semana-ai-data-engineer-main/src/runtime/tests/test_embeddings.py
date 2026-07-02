from .embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel
)


model = SentenceTransformerEmbeddingModel()

vectors = model.encode([
    "Pydantic BaseModel",
    "Create ShopAgent models",
])

print()

print("=" * 80)
print("EMBEDDINGS")
print("=" * 80)

print(f"Dimension : {model.dimension}")

print(f"Shape     : {vectors.shape}")

print()

print(vectors[0][:10])