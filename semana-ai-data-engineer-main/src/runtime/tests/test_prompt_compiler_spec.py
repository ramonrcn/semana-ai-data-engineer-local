from copy import deepcopy
from pathlib import Path

from src.runtime.context import RuntimeContext
from src.runtime.models import Capability
from src.runtime.knowledge.models import KnowledgeDocument
from src.runtime.knowledge.retrieved import RetrievedKnowledge
from src.runtime.prompt.prompt import Prompt
from src.runtime.prompt_compiler.compiler import PromptCompiler


def build_capability() -> Capability:
    return Capability(
        id="test.capability",
        name="Test Capability",
        category="test",
        description=(
            "Capability used by PromptCompiler "
            "specification tests."
        ),
        tools=[
            "Read",
            "Write",
        ],
        model="test-model",
        prompt=(
            "You are a deterministic test capability."
        ),
        source_path=Path(
            "test-capability.md"
        ),
    )


def build_knowledge(
    document_id: str,
    content: str,
    *,
    score: float | None = None,
    rank: int | None = None,
) -> RetrievedKnowledge:

    document = KnowledgeDocument(
        id=document_id,
        title=document_id,
        content=content,
        source_path=Path(
            f"{document_id}.md"
        ),
    )

    return RetrievedKnowledge(
        document=document,
        score=score,
        rank=rank,
    )


def build_context(
    *,
    objective: str = (
        "Build the requested feature."
    ),
    knowledge: list[RetrievedKnowledge] | None = None,
) -> RuntimeContext:

    if knowledge is None:
        knowledge = [
            build_knowledge(
                document_id="knowledge.first",
                content=(
                    "First knowledge document."
                ),
                score=0.9,
                rank=1,
            ),
            build_knowledge(
                document_id="knowledge.second",
                content=(
                    "Second knowledge document."
                ),
                score=0.8,
                rank=2,
            ),
        ]

    return RuntimeContext(
        capability=build_capability(),
        objective=objective,
        knowledge=knowledge,
        environment_tools=[
            "Read",
            "Write",
        ],
    )


def test_compile_returns_prompt():

    compiler = PromptCompiler()
    context = build_context()

    result = compiler.compile(
        context
    )

    assert isinstance(
        result,
        Prompt,
    )


def test_prompt_is_non_empty():

    compiler = PromptCompiler()
    context = build_context()

    prompt = compiler.compile(
        context
    )

    assert prompt.text
    assert prompt.text.strip()


def test_required_sections_are_present():

    compiler = PromptCompiler()
    context = build_context()

    prompt = compiler.compile(
        context
    ).text

    assert "# SYSTEM" in prompt
    assert "# EXECUTION RULES" in prompt


def test_sections_follow_specified_order():

    compiler = PromptCompiler()
    context = build_context()

    prompt = compiler.compile(
        context
    ).text

    system_index = prompt.index(
        "# SYSTEM"
    )

    execution_rules_index = prompt.index(
        "# EXECUTION RULES"
    )

    objective_index = prompt.index(
        "# OBJECTIVE"
    )

    knowledge_index = prompt.index(
        "# REFERENCE KNOWLEDGE"
    )

    assert (
        system_index
        < execution_rules_index
        < objective_index
        < knowledge_index
    )


def test_capability_prompt_is_preserved():

    compiler = PromptCompiler()
    context = build_context()

    prompt = compiler.compile(
        context
    ).text

    assert (
        context.capability.prompt
        in prompt
    )


def test_objective_is_preserved():

    compiler = PromptCompiler()

    objective = (
        "Create exactly three "
        "Pydantic models."
    )

    context = build_context(
        objective=objective
    )

    prompt = compiler.compile(
        context
    ).text

    assert objective in prompt


def test_empty_objective_omits_objective_section():

    compiler = PromptCompiler()

    context = build_context(
        objective=""
    )

    prompt = compiler.compile(
        context
    ).text

    assert "# OBJECTIVE" not in prompt


def test_selected_knowledge_is_preserved():

    compiler = PromptCompiler()

    first = build_knowledge(
        document_id="knowledge.first",
        content="Unique first content.",
    )

    second = build_knowledge(
        document_id="knowledge.second",
        content="Unique second content.",
    )

    context = build_context(
        knowledge=[
            first,
            second,
        ]
    )

    prompt = compiler.compile(
        context
    ).text

    assert (
        "## knowledge.first"
        in prompt
    )

    assert (
        "Unique first content."
        in prompt
    )

    assert (
        "## knowledge.second"
        in prompt
    )

    assert (
        "Unique second content."
        in prompt
    )


def test_empty_knowledge_omits_reference_knowledge_section():

    compiler = PromptCompiler()

    context = build_context(
        knowledge=[]
    )

    prompt = compiler.compile(
        context
    ).text

    assert (
        "# REFERENCE KNOWLEDGE"
        not in prompt
    )


def test_knowledge_order_is_preserved():

    compiler = PromptCompiler()

    context = build_context(
        knowledge=[
            build_knowledge(
                document_id="knowledge.third",
                content="Third",
                rank=3,
            ),
            build_knowledge(
                document_id="knowledge.first",
                content="First",
                rank=1,
            ),
            build_knowledge(
                document_id="knowledge.second",
                content="Second",
                rank=2,
            ),
        ]
    )

    prompt = compiler.compile(
        context
    ).text

    third_index = prompt.index(
        "## knowledge.third"
    )

    first_index = prompt.index(
        "## knowledge.first"
    )

    second_index = prompt.index(
        "## knowledge.second"
    )

    assert (
        third_index
        < first_index
        < second_index
    )


def test_duplicate_knowledge_is_preserved():

    compiler = PromptCompiler()

    duplicated = build_knowledge(
        document_id="knowledge.duplicate",
        content="Duplicated content.",
    )

    context = build_context(
        knowledge=[
            duplicated,
            duplicated,
        ]
    )

    prompt = compiler.compile(
        context
    ).text

    assert (
        prompt.count(
            "## knowledge.duplicate"
        )
        == 2
    )

    assert (
        prompt.count(
            "Duplicated content."
        )
        == 2
    )


def test_equivalent_context_produces_equivalent_prompt():

    compiler = PromptCompiler()

    first_context = build_context()
    second_context = build_context()

    first_prompt = compiler.compile(
        first_context
    )

    second_prompt = compiler.compile(
        second_context
    )

    assert (
        first_prompt.text
        == second_prompt.text
    )


def test_repeated_compilation_is_deterministic():

    compiler = PromptCompiler()
    context = build_context()

    first_prompt = compiler.compile(
        context
    )

    second_prompt = compiler.compile(
        context
    )

    assert (
        first_prompt.text
        == second_prompt.text
    )


def test_compile_does_not_mutate_context():

    compiler = PromptCompiler()

    context = build_context()

    original_context = deepcopy(
        context
    )

    compiler.compile(
        context
    )

    assert (
        context
        == original_context
    )


def test_prompt_does_not_expose_internal_object_representations():

    compiler = PromptCompiler()
    context = build_context()

    prompt = compiler.compile(
        context
    ).text

    assert "Prompt(" not in prompt

    assert (
        "RetrievedKnowledge("
        not in prompt
    )

    assert (
        "KnowledgeDocument("
        not in prompt
    )

def test_prompt_supports_utf8_content():

    compiler = PromptCompiler()

    objective = (
        "Analise o preço do veículo em São Paulo. "
        "Comparação: ação, combustível, câmbio. "
        "日本語 🚗💨"
    )

    knowledge = [
        build_knowledge(
            document_id="knowledge.utf8",
            content=(
                "Volkswagen Golf preparado: "
                "injeção, pressão e potência. "
                "日本語 🚗💨"
            ),
        )
    ]

    context = build_context(
        objective=objective,
        knowledge=knowledge,
    )

    prompt = compiler.compile(
        context
    ).text

    encoded = prompt.encode(
        "utf-8"
    )

    decoded = encoded.decode(
        "utf-8"
    )

    assert decoded == prompt
    assert objective in prompt
    assert knowledge[0].document.content in prompt

def test_large_knowledge_context_is_preserved():

    compiler = PromptCompiler()

    large_content = (
        "large-knowledge-content "
        * 10_000
    )

    knowledge = [
        build_knowledge(
            document_id="knowledge.large",
            content=large_content,
        )
    ]

    context = build_context(
        knowledge=knowledge,
    )

    prompt = compiler.compile(
        context
    ).text

    assert large_content in prompt

    assert (
        prompt.count(
            "large-knowledge-content"
        )
        == 10_000
    )