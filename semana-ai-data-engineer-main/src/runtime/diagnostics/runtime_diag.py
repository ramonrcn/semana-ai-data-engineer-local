from src.runtime.knowledge.embedding import EmbeddingKnowledgeSelector

from src.runtime.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)
from .testing import build_test_runtime
from src.runtime.llm.ollama import OllamaLLM


CAPABILITY = "domain.shopagent-builder"

OBJECTIVE = "Create Pydantic models for ShopAgent"


runtime = build_test_runtime(
    
    llm=OllamaLLM(),
    
    selector=EmbeddingKnowledgeSelector(

        embedding_model=SentenceTransformerEmbeddingModel(),

        top_k=5,

    )

)


response = runtime.run(

    CAPABILITY,

    OBJECTIVE,

)


print("\n" + "=" * 80)
print("LLM RESPONSE")
print("=" * 80)

print(response)