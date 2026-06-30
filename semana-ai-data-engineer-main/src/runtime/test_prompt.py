from pathlib import Path

from .knowledge.selector import BaseKnowledgeSelector
from .knowledge.tfidf import TFIDFKnowledgeSelector
from .knowledge.lsa import LSAKnowledgeSelector
from .knowledge.embedding import EmbeddingKnowledgeSelector
from .embeddings.sentence_transformer import (
    SentenceTransformerEmbeddingModel,
)
# from .knowledge.keyword import KeywordKnowledgeSelector
# from .knowledge.passthrough import PassthroughKnowledgeSelector

from .testing import build_test_runtime


CAPABILITY = "domain.shopagent-builder"
OBJECTIVE = "Create Pydantic models for ShopAgent"


# ============================================================================
# Choose the selector under evaluation.
# ============================================================================

SELECTOR: BaseKnowledgeSelector = EmbeddingKnowledgeSelector(
    embedding_model=SentenceTransformerEmbeddingModel(),
    top_k=5,
)


# Examples:
#
# SELECTOR = PassthroughKnowledgeSelector()
# SELECTOR = FirstKKnowledgeSelector(k=5)
# SELECTOR = KeywordKnowledgeSelector(top_k=5)
# SELECTOR = TFIDFKnowledgeSelector(top_k=5)
# SELECTOR = LSAKnowledgeSelector(top_k=5)


# ============================================================================
# Build runtime
# ============================================================================

runtime = build_test_runtime(
    selector=SELECTOR,
)


# ============================================================================
# Diagnostics
# ============================================================================

print("\n" + "=" * 80)
print("KNOWLEDGE SELECTOR")
print("=" * 80)

print(runtime.knowledge_selector.__class__.__name__)


# ============================================================================
# Build execution context
# ============================================================================

context = runtime.build_context(
    CAPABILITY,
    OBJECTIVE,
)


print("\n" + "=" * 80)
print("CAPABILITY")
print("=" * 80)

print(context.capability.id)


print("\n" + "=" * 80)
print("KNOWLEDGE DOCUMENTS")
print("=" * 80)

total_chars = 0

for document in context.knowledge:

    chars = len(document.content)
    total_chars += chars

    print(
        f"{document.id:<60} {chars:>8} chars"
    )


print("\n" + "=" * 80)
print("KNOWLEDGE SUMMARY")
print("=" * 80)

print(
    f"Documents loaded : {len(context.knowledge)}"
)

print(
    f"Knowledge size   : {total_chars:,} chars"
)


# ============================================================================
# Assemble prompt
# ============================================================================

prompt = runtime.assemble_prompt(
    CAPABILITY,
    OBJECTIVE,
)


# ============================================================================
# Persist prompt
# ============================================================================

artifacts = Path("artifacts")
artifacts.mkdir(exist_ok=True)

prompt_path = artifacts / "compiled_prompt.md"

prompt_path.write_text(
    prompt,
    encoding="utf-8",
)


# ============================================================================
# Prompt diagnostics
# ============================================================================

print("\n" + "=" * 80)
print("PROMPT SUMMARY")
print("=" * 80)

print()

print(
    f"Knowledge Selector : "
    f"{runtime.knowledge_selector.__class__.__name__}"
)

print(
    f"Documents          : {len(context.knowledge)}"
)

print(
    f"Knowledge size     : {total_chars:,} chars"
)

print(
    f"Prompt size        : {len(prompt):,} chars"
)

print(
    f"Knowledge ratio    : {total_chars / len(prompt):.1%}"
)

print(
    f"Prompt file        : {prompt_path}"
)
# NOTE:
# assemble_prompt() currently rebuilds the RuntimeContext internally.
# This duplication will be removed during the Runtime API Refactoring sprint.