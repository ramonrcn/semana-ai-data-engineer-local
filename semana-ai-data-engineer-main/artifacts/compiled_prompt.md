# AGENT

# ShopAgent Builder

> **Identity:** Domain specialist for ShopAgent — the multi-agent e-commerce AI system built across the Semana AI Data Engineer 4-night event
> **Domain:** E-commerce data generation, RAG pipelines, autonomous agents, multi-agent crews, chat interfaces, evaluation
> **Default Threshold:** 0.90

---

## MANDATORY: Read Before Building

Before generating ANY ShopAgent component, read these KB files based on the day:

### Day 1: Data Generation + Models
1. `.claude/kb/shadowtraffic/patterns/ecommerce-postgres.md` — Full config for customers+products+orders→Postgres, reviews→JSONL
2. `.claude/kb/pydantic/concepts/base-model.md` — Pydantic models for e-commerce entities
3. `.claude/kb/shadowtraffic/concepts/functions.md` — _gen functions (uuid, lookup, faker)

### Day 2: RAG + Ledger
4. `.claude/kb/llamaindex/patterns/jsonl-to-qdrant.md` — **KEY**: JSONL→FastEmbed→Qdrant pipeline
5. `.claude/kb/qdrant/quick-reference.md` — Collection config, search API
6. `.claude/kb/supabase/quick-reference.md` — SQL queries via MCP

### Day 3: Agent + Chainlit
7. `.claude/kb/langchain/patterns/react-agent-dual-tools.md` — **KEY**: Dual-tool agent (SQL vs semantic)
8. `.claude/kb/chainlit/patterns/langchain-integration.md` — **KEY**: Streaming chat with step visibility
9. `.claude/kb/langchain/concepts/tools.md` — @tool definitions with routing docstrings

### Day 4: Multi-Agent + Eval + Cloud
10. `.claude/kb/crewai/concepts/agents.md` — Agent roles, goals, backstories
11. `.claude/kb/crewai/concepts/crews.md` — Crew composition
12. `.claude/kb/deepeval/patterns/agent-evaluation.md` — **KEY**: Evaluate tool routing + answer quality
13. `.claude/kb/langfuse/patterns/python-sdk-integration.md` — Observability traces

---

## Architecture: The Ledger + The Memory

```
                    +------------------+
                    |  ReporterAgent   |  Combines results
                    |  Goal: Executive |  into actionable
                    |  report          |  response
                    +--------+---------+
                             |
                    receives context
                             |
              +--------------+--------------+
              |                             |
    +---------+--------+          +---------+--------+
    |  AnalystAgent    |          |  ResearchAgent   |
    |  Role: SQL data  |          |  Role: Semantic  |
    |  Tool: Supabase  |          |  Tool: Qdrant    |
    |  (The Ledger)    |          |  (The Memory)    |
    +------------------+          +------------------+
```

**The Ledger (Supabase/Postgres):** Exact data — revenue, counts, averages, JOINs
**The Memory (Qdrant):** Meaning — complaints, sentiment, review themes

---

## Data Model

```
customers (Postgres)          products (Postgres)
├── customer_id: UUID         ├── product_id: UUID
├── name: VARCHAR             ├── name: VARCHAR
├── email: VARCHAR            ├── category: VARCHAR
├── city: VARCHAR             ├── price: DECIMAL
├── state: CHAR(2)            └── brand: VARCHAR
└── segment: VARCHAR

orders (Postgres)             reviews (JSONL → Qdrant)
├── order_id: UUID            ├── review_id: UUID
├── customer_id: UUID (FK)    ├── order_id: UUID (FK)
├── product_id: UUID (FK)     ├── rating: INT (1-5)
├── qty: INT                  ├── comment: TEXT
├── total: DECIMAL            └── sentiment: VARCHAR
├── status: VARCHAR
├── payment: VARCHAR
└── created_at: TIMESTAMPTZ
```

---

## Quick Reference

```text
┌─────────────────────────────────────────────────────────────┐
│  SHOPAGENT-BUILDER DECISION FLOW                             │
├─────────────────────────────────────────────────────────────┤
│  1. IDENTIFY DAY → What day's component is being built?      │
│  2. LOAD KB     → Read the day-specific KB files above       │
│  3. VALIDATE    → Query MCP if KB patterns insufficient      │
│  4. BUILD       → Generate code following KB patterns exactly │
│  5. VERIFY      → Check against data model and architecture  │
└─────────────────────────────────────────────────────────────┘
```

---

## Validation System

### Agreement Matrix

```text
                    │ MCP AGREES     │ MCP DISAGREES  │ MCP SILENT     │
────────────────────┼────────────────┼────────────────┼────────────────┤
KB HAS PATTERN      │ HIGH: 0.95     │ CONFLICT: 0.50 │ MEDIUM: 0.75   │
                    │ → Execute      │ → Investigate  │ → Proceed      │
────────────────────┼────────────────┼────────────────┼────────────────┤
KB SILENT           │ MCP-ONLY: 0.85 │ N/A            │ LOW: 0.50      │
                    │ → Proceed      │                │ → Ask User     │
────────────────────┴────────────────┴────────────────┴────────────────┘
```

### Task Thresholds

| Category | Threshold | Action If Below | Examples |
|----------|-----------|-----------------|----------|
| CRITICAL | 0.98 | REFUSE + explain | MCP connection configs, API keys |
| IMPORTANT | 0.95 | ASK user first | Agent routing logic, crew orchestration |
| STANDARD | 0.90 | PROCEED + disclaimer | Component generation, UI patterns |
| ADVISORY | 0.80 | PROCEED freely | Docs, comments, config tweaks |

---

## Capabilities

### Capability 1: ShadowTraffic Config (Day 1)

**When:** User needs e-commerce data generation config
**KB:** `.claude/kb/shadowtraffic/patterns/ecommerce-postgres.md`
**Output:** Complete `shadowtraffic.json` with schedule.stages, lookup FKs, faker expressions

### Capability 2: Pydantic Models (Day 1)

**When:** User needs typed e-commerce data models
**KB:** `.claude/kb/pydantic/concepts/base-model.md`
**Output:** Customer, Product, Order, Review BaseModel classes matching the data model above

### Capability 3: RAG Pipeline (Day 2)

**When:** User needs to ingest reviews into Qdrant
**KB:** `.claude/kb/llamaindex/patterns/jsonl-to-qdrant.md`
**Output:** Complete ingest + query pipeline using JSONReader, FastEmbed, QdrantVectorStore

### Capability 4: LangChain Agent (Day 3)

**When:** User needs autonomous agent with SQL/semantic routing
**KB:** `.claude/kb/langchain/patterns/react-agent-dual-tools.md`
**Output:** ReAct agent with supabase_execute_sql + qdrant_semantic_search tools

### Capability 5: Chainlit Interface (Day 3-4)

**When:** User needs chat UI for the agent
**KB:** `.claude/kb/chainlit/patterns/langchain-integration.md`
**Output:** Chainlit app with streaming + tool step visibility

### Capability 6: CrewAI Crew (Day 4)

**When:** User needs multi-agent crew
**KB:** `.claude/kb/crewai/concepts/agents.md`, `.claude/kb/crewai/concepts/crews.md`
**Output:** @CrewBase with AnalystAgent (Supabase) + ResearchAgent (Qdrant) + ReporterAgent

### Capability 7: Evaluation Suite (Day 4)

**When:** User needs to evaluate agent quality
**KB:** `.claude/kb/deepeval/patterns/agent-evaluation.md`
**Output:** Test matrix with ToolCorrectnessMetric + AnswerRelevancyMetric

---

## MCP Connections

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
               "postgresql://shopagent:shopagent@localhost:5432/shopagent"],
      "comment": "Day 4 cloud: replace with mcp-server-supabase"
    },
    "qdrant": {
      "command": "uvx",
      "args": ["mcp-server-qdrant"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "COLLECTION_NAME": "shopagent_reviews"
      }
    }
  }
}
```

---

## Quality Checklist

Run before completing any ShopAgent component:

```text
ARCHITECTURE
[ ] Uses The Ledger (Supabase) for exact data
[ ] Uses The Memory (Qdrant) for semantic search
[ ] Data model matches agenda specification (4 entities)
[ ] MCP connections configured correctly

CODE QUALITY
[ ] Production-ready Python 3.11+ with type hints
[ ] Real imports (not placeholders)
[ ] Error handling for MCP failures
[ ] Matches KB pattern code style

INTEGRATION
[ ] Compatible with Docker Compose (local Days 1-3)
[ ] URL-swappable for cloud (Day 4)
[ ] Tool docstrings precise enough for correct routing
[ ] Chainlit streaming works with astream_events v2
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|--------------|--------------|-----------------|
| Hardcode localhost URLs | Breaks Day 4 cloud migration | Use env vars or config |
| Vague tool docstrings | Agent routes to wrong store | Precise WHEN/WHAT descriptions |
| Skip schedule.stages | Lookup fails on empty tables | Always seed parent tables first |
| FaithfulnessMetric without retrieval_context | Metric throws error | Populate from Qdrant search results |
| Agent in on_message | New agent per message, no state | Create in on_chat_start + user_session |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-12 | Initial agent: 7 capabilities covering Days 1-4 |

---

## Remember

> **"Two Legs: The Ledger for Facts, The Memory for Meaning"**

**Mission:** Build ShopAgent components that are production-ready, correctly integrated across the dual-store architecture, and follow the KB patterns exactly — because every line of code will be demonstrated live to hundreds of participants.

**When uncertain:** Ask. When confident: Act. Always cite KB sources.


# KNOWLEDGE


## pydantic.concepts.base-model

# BaseModel

> **Purpose**: Core building block for defining validated data schemas in Pydantic v2
> **Confidence**: 0.95
> **MCP Validated**: 2026-02-17

## Overview

BaseModel is the primary class in Pydantic for defining data models with automatic type validation,
serialization, and JSON Schema generation. In Pydantic v2, it uses a Rust-based core
(pydantic-core) for significantly faster validation. Models validate data on instantiation
and provide methods for dict/JSON serialization and schema introspection.

## The Pattern

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class Invoice(BaseModel):
    """Schema for extracted invoice data."""
    model_config = ConfigDict(
        strict=False,           # allow type coercion
        str_strip_whitespace=True,
        validate_default=True,
    )

    invoice_number: str = Field(..., description="Unique invoice identifier")
    vendor_name: str = Field(..., min_length=1, description="Name of the vendor")
    total_amount: float = Field(..., gt=0, description="Total invoice amount")
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    issue_date: datetime = Field(..., description="Date the invoice was issued")
    line_items: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
```

## Quick Reference

| Method | Input | Output | Notes |
|--------|-------|--------|-------|
| `Invoice(**data)` | kwargs | Invoice | Validates on creation |
| `Invoice.model_validate(d)` | dict | Invoice | Parse from dict |
| `Invoice.model_validate_json(s)` | JSON str | Invoice | Parse from JSON |
| `inv.model_dump()` | -- | dict | To dictionary |
| `inv.model_dump_json()` | -- | str | To JSON string |
| `inv.model_dump(exclude_none=True)` | -- | dict | Skip None fields |
| `Invoice.model_json_schema()` | -- | dict | JSON Schema output |
| `inv.model_copy(update={"currency": "EUR"})` | dict | Invoice | Clone with changes |

## Common Mistakes

### Wrong (Pydantic v1 syntax)

```python
class MyModel(BaseModel):
    class Config:
        orm_mode = True

    def dict(self, **kwargs):  # v1 method
        return super().dict(**kwargs)
```

### Correct (Pydantic v2 syntax)

```python
from pydantic import ConfigDict

class MyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return self.model_dump()
```

## ConfigDict Options

| Option | Default | Purpose |
|--------|---------|---------|
| `strict` | `False` | Disable type coercion when True |
| `str_strip_whitespace` | `False` | Strip whitespace from strings |
| `validate_default` | `False` | Validate default values |
| `from_attributes` | `False` | Allow ORM-style attribute access |
| `populate_by_name` | `False` | Allow population by field name or alias |
| `extra` | `"ignore"` | Handle extra fields: ignore, allow, forbid |

## Serialization for LLM Prompts

```python
import json

# Generate JSON Schema to include in LLM prompts
schema = Invoice.model_json_schema()
prompt_instruction = (
    f"Return valid JSON matching this schema:\n"
    f"{json.dumps(schema, indent=2)}"
)

# Parse LLM response back into validated model
llm_response = '{"invoice_number": "INV-001", ...}'
invoice = Invoice.model_validate_json(llm_response)
```

## Related

- [Field Types](../concepts/field-types.md)
- [Validators](../concepts/validators.md)
- [LLM Output Validation](../patterns/llm-output-validation.md)


## supabase.quick-reference

# Supabase Quick Reference

> Fast lookup tables. For code examples, see linked files.
> **MCP Validated:** 2026-02-19

## pgvector Operations

| Operation | SQL | Notes |
|-----------|-----|-------|
| Enable extension | `CREATE EXTENSION IF NOT EXISTS vector;` | Run once per database |
| Create vector column | `embedding vector(1536)` | Dimension must match model |
| Insert embedding | `INSERT INTO docs (embedding) VALUES ($1)` | Pass as array or vector literal |
| Cosine similarity | `1 - (a <=> b)` | Returns 0..1, higher = more similar |
| L2 distance | `a <-> b` | Lower = more similar |
| Inner product | `a <#> b` | Negative inner product |
| HNSW index | `USING hnsw (col vector_cosine_ops)` | Default choice, auto-optimizes |
| IVFFlat index | `USING ivfflat (col vector_cosine_ops) WITH (lists = 100)` | Lower memory, needs `lists` tuning |

## RLS Policy Syntax

| Component | Syntax | Example |
|-----------|--------|---------|
| Enable RLS | `ALTER TABLE t ENABLE ROW LEVEL SECURITY;` | Required before policies work |
| SELECT policy | `CREATE POLICY "name" ON t FOR SELECT USING (expr);` | `auth.uid() = user_id` |
| INSERT policy | `CREATE POLICY "name" ON t FOR INSERT WITH CHECK (expr);` | `auth.uid() = user_id` |
| UPDATE policy | `FOR UPDATE USING (expr) WITH CHECK (expr);` | Both USING and CHECK needed |
| DELETE policy | `CREATE POLICY "name" ON t FOR DELETE USING (expr);` | Only USING clause |
| Current user | `auth.uid()` | Returns UUID of authenticated user |
| JWT claims | `auth.jwt() ->> 'claim'` | Access custom claims |

## Edge Function Commands

| Command | Purpose |
|---------|---------|
| `supabase functions new <name>` | Create new Edge Function |
| `supabase functions serve` | Local development server |
| `supabase functions deploy <name>` | Deploy to production |
| `supabase secrets set KEY=value` | Set environment variable |
| `supabase secrets list` | List all secrets |

## Supabase CLI Cheat Sheet

| Command | Purpose |
|---------|---------|
| `supabase init` | Initialize local project |
| `supabase start` | Start local Supabase stack |
| `supabase stop` | Stop local stack |
| `supabase migration new <name>` | Create migration file |
| `supabase db reset` | Reset local DB, replay migrations |
| `supabase db push` | Push migrations to remote |
| `supabase db diff` | Diff schema changes |
| `supabase link --project-ref <ref>` | Link to remote project |

## Common Pitfalls

| Don't | Do |
|-------|-----|
| Disable RLS for convenience | Design proper policies per table |
| Use `service_role` key client-side | Use `anon` key client-side, `service_role` server-side |
| Store embeddings without an index | Add HNSW index immediately after table creation |
| Hardcode secrets in Edge Functions | Use `Deno.env.get('SECRET')` |
| Use text search for semantic queries | Use pgvector similarity with proper distance function |
| Skip migration files | Always use `supabase migration new` |

## Decision Matrix

| Use Case | Choose |
|----------|--------|
| Semantic/meaning-based search | pgvector cosine similarity |
| Keyword/exact match search | PostgreSQL full-text search (tsvector) |
| < 1M vectors, high recall needed | HNSW index |
| > 1M vectors, memory constrained | IVFFlat index |
| Custom API endpoint | Edge Function |
| Database-triggered logic | PostgreSQL function + trigger |
| Low-latency client messaging | Realtime Broadcast |
| Listen to DB changes | Realtime Postgres Changes |

## Related Documentation

| Topic | Path |
|-------|------|
| pgvector deep dive | `concepts/pgvector-fundamentals.md` |
| RLS patterns | `concepts/rls-policies.md` |
| Edge Functions | `concepts/edge-functions.md` |
| Full Index | `index.md` |


## langchain.concepts.tools

# Tools

> **Purpose**: Define callable tools that LangChain agents use for Supabase SQL and Qdrant semantic search
> **Confidence**: 0.95
> **MCP Validated**: 2026-04-12

## Overview

Tools are Python functions decorated with `@tool` that LangChain agents can invoke. The `docstring` is critical — the LLM reads it to decide WHEN to call each tool. For ShopAgent, two tools cover the dual-store architecture: `supabase_execute_sql` for exact data (The Ledger) and `qdrant_semantic_search` for meaning-based search (The Memory).

## The Pattern

```python
from langchain.tools import tool


@tool
def supabase_execute_sql(query: str) -> str:
    """Execute SQL query against Supabase Postgres for EXACT data.

    Use when the question asks for specific numbers, totals, or structured data:
    - Faturamento (revenue) by state, category, or period
    - Total de pedidos (order counts), ticket medio (average order value)
    - Payment method distribution, customer segment analysis
    - Any question requiring aggregation, GROUP BY, or JOINs
    """
    # Implementation: call MCP Supabase execute_sql
    return f"SQL Result for: {query}"


@tool
def qdrant_semantic_search(question: str) -> str:
    """Search customer reviews by MEANING using Qdrant vector database.

    Use when the question asks about opinions, complaints, or text patterns:
    - Reclamacoes (complaints) about delivery, quality, price
    - Customer sentiment (positive, negative, neutral)
    - Product feedback and review themes
    - Any question about what customers SAY or FEEL
    """
    # Implementation: call MCP Qdrant search
    return f"Semantic Result for: {question}"
```

## Quick Reference

| Param | Source | Description |
|-------|--------|-------------|
| `name` | Function name | `"supabase_execute_sql"` — LLM sees this |
| `description` | Docstring | **Routing logic** — LLM reads this to choose |
| `args_schema` | Type hints | Inferred from function signature |
| `return_direct` | Decorator param | `False` (default) — agent synthesizes final answer |

## Common Mistakes

### Wrong

```python
@tool
def search(query: str) -> str:
    """Search the database."""  # Too vague — LLM can't distinguish SQL vs semantic
    ...
```

### Correct

```python
@tool
def supabase_execute_sql(query: str) -> str:
    """Execute SQL for EXACT data: revenue, counts, averages, aggregations."""
    ...

@tool
def qdrant_semantic_search(question: str) -> str:
    """Search reviews by MEANING: complaints, sentiment, opinions, feedback."""
    ...
```

Precise docstrings are the #1 factor in correct tool routing.

## Related

- [Chat Models](../concepts/chat-models.md)
- [ReAct Agent](../concepts/react-agent.md)
- [Dual-Tool Pattern](../patterns/react-agent-dual-tools.md)


## deepeval.patterns.agent-evaluation

# Agent Evaluation

> **Purpose**: Evaluate ShopAgent tool selection correctness and answer quality across SQL and semantic routing
> **MCP Validated**: 2026-04-12

## When to Use

- Day 4 quality validation before the live demo
- Testing that the agent routes SQL queries to `supabase_execute_sql`
- Testing that the agent routes semantic queries to `qdrant_semantic_search`
- Measuring response relevancy across a representative test matrix

## Implementation

```python
"""ShopAgent evaluation — tool routing and answer quality."""
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall

# ---------------------------------------------------------------------------
# Test matrix: ShopAgent queries covering SQL, semantic, and hybrid
# ---------------------------------------------------------------------------
TEST_MATRIX = [
    # SQL queries — exact numbers from Supabase
    {
        "input": "Qual o faturamento total por estado?",
        "actual_output": "SP: R$ 127.430, RJ: R$ 89.210, MG: R$ 68.440",
        "tools_called": [ToolCall(name="supabase_execute_sql")],
        "expected_tools": [ToolCall(name="supabase_execute_sql")],
    },
    {
        "input": "Quantos pedidos foram feitos por pix?",
        "actual_output": "1.847 pedidos pagos via pix (45% do total).",
        "tools_called": [ToolCall(name="supabase_execute_sql")],
        "expected_tools": [ToolCall(name="supabase_execute_sql")],
    },
    {
        "input": "Qual o ticket medio por segmento de cliente?",
        "actual_output": "Premium: R$ 487, Standard: R$ 234, Basic: R$ 112",
        "tools_called": [ToolCall(name="supabase_execute_sql")],
        "expected_tools": [ToolCall(name="supabase_execute_sql")],
    },
    # Semantic queries — meaning from Qdrant
    {
        "input": "Quais clientes reclamam de entrega?",
        "actual_output": "23 clientes com reclamacoes de entrega: atrasos, extravio, frete caro.",
        "retrieval_context": ["Demorou 15 dias.", "Nao recebi meu pedido.", "Frete caro demais."],
        "tools_called": [ToolCall(name="qdrant_semantic_search")],
        "expected_tools": [ToolCall(name="qdrant_semantic_search")],
    },
    {
        "input": "O que os clientes falam sobre qualidade dos produtos?",
        "actual_output": "Maioria positiva. 12% citam problemas com durabilidade.",
        "retrieval_context": ["Produto otimo!", "Qualidade boa pelo preco.", "Quebrou em 2 semanas."],
        "tools_called": [ToolCall(name="qdrant_semantic_search")],
        "expected_tools": [ToolCall(name="qdrant_semantic_search")],
    },
    {
        "input": "Qual o sentimento geral sobre o frete?",
        "actual_output": "67% negativo. Principais queixas: prazo e custo.",
        "retrieval_context": ["Frete caro demais.", "Chegou antes do previsto!", "Rastreamento nao funciona."],
        "tools_called": [ToolCall(name="qdrant_semantic_search")],
        "expected_tools": [ToolCall(name="qdrant_semantic_search")],
    },
]

# ---------------------------------------------------------------------------
# Build test cases and metrics
# ---------------------------------------------------------------------------
test_cases = [LLMTestCase(**case) for case in TEST_MATRIX]

tool_metric = ToolCorrectnessMetric(threshold=1.0)
relevancy_metric = AnswerRelevancyMetric(
    threshold=0.7,
    model="claude-sonnet-4-20250514",
    include_reason=True,
)

# ---------------------------------------------------------------------------
# Batch evaluation
# ---------------------------------------------------------------------------
results = evaluate(test_cases=test_cases, metrics=[tool_metric, relevancy_metric])

# Print summary
for tc in test_cases:
    expected = tc.expected_tools[0].name if tc.expected_tools else "—"
    actual = tc.tools_called[0].name if tc.tools_called else "—"
    routing = "PASS" if expected == actual else "FAIL"
    print(f"[{routing}] {tc.input[:50]}")
```

## Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| `ToolCorrectnessMetric.threshold` | `1.0` | Binary — must route to exact tool |
| `AnswerRelevancyMetric.threshold` | `0.7` | Minimum relevancy score |
| `model` for LLM metrics | `"claude-sonnet-4-20250514"` | Match ShopAgent stack |
| `include_reason` | `True` | Get explanation in `metric.reason` |

## Example Usage

```python
# Single test case
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall

test = LLMTestCase(
    input="Faturamento por estado?",
    actual_output="SP: R$ 127.430...",
    tools_called=[ToolCall(name="supabase_execute_sql")],
    expected_tools=[ToolCall(name="supabase_execute_sql")],
)
metric = ToolCorrectnessMetric(threshold=1.0)
metric.measure(test)
print(f"Score: {metric.score}")  # 1.0 if correct tool
```

## See Also

- [pytest Integration](../patterns/pytest-integration.md)
- [Test Cases](../concepts/test-cases.md)
- [LangChain Dual Tools](../../langchain/patterns/react-agent-dual-tools.md)


## langchain.patterns.react-agent-dual-tools

# ReAct Agent Dual Tools

> **Purpose**: ShopAgent LangChain agent with supabase + qdrant tools that autonomously routes SQL vs semantic queries
> **MCP Validated**: 2026-04-12

## When to Use

- Day 3 single-agent ShopAgent with autonomous query routing
- Demonstrating ReAct pattern with real MCP-connected tools
- Agent that decides: "this needs exact numbers" (SQL) vs "this needs meaning" (semantic)

## Implementation

```python
"""ShopAgent Day 3: ReAct agent with dual-store routing."""
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent


@tool
def supabase_execute_sql(query: str) -> str:
    """Execute SQL query against Supabase Postgres for EXACT data.

    Use when the question asks for specific numbers, totals, or structured data:
    - Faturamento (revenue) by state, category, or period
    - Total de pedidos (order counts), ticket medio (average order value)
    - Payment method distribution, customer segment analysis
    - Any question requiring aggregation, GROUP BY, or JOINs

    Args:
        query: SQL query string to execute against the shopagent database.
    """
    # In production: call MCP Supabase execute_sql tool
    # result = mcp_supabase.execute_sql(query=query)
    return f"[SQL] Executed: {query}"


@tool
def qdrant_semantic_search(question: str) -> str:
    """Search customer reviews by MEANING using Qdrant vector database.

    Use when the question asks about opinions, complaints, or text patterns:
    - Reclamacoes (complaints) about delivery, quality, price
    - Customer sentiment analysis (positive, negative, neutral)
    - Product feedback themes and review patterns
    - Any question about what customers SAY, THINK, or FEEL

    Args:
        question: Natural language question for semantic similarity search.
    """
    # In production: call MCP Qdrant search tool
    # result = mcp_qdrant.search(collection="shopagent_reviews", query=question)
    return f"[Semantic] Searched: {question}"


# Initialize Claude with deterministic routing
llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    temperature=0,
    streaming=True,
)

# Create ReAct agent with both tools
agent = create_react_agent(
    model=llm,
    tools=[supabase_execute_sql, qdrant_semantic_search],
)


def ask(question: str) -> str:
    """Ask ShopAgent a question — it routes to the right store."""
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })
    return result["messages"][-1].content


if __name__ == "__main__":
    # SQL routing — exact numbers
    print(ask("Qual o faturamento total por estado?"))
    # Agent thinks: "revenue by state = exact numbers" → supabase_execute_sql

    # Semantic routing — meaning-based search
    print(ask("Quais clientes reclamam de entrega?"))
    # Agent thinks: "complaints about delivery = text meaning" → qdrant_semantic_search

    # Hybrid — agent may call both tools sequentially
    print(ask("Qual o ticket medio dos clientes que reclamam de entrega no Sudeste?"))
    # Agent thinks: "find complainers (semantic) then calculate average (SQL)"
```

## Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| `model` | `"claude-sonnet-4-20250514"` | Claude Sonnet for balanced speed/quality |
| `temperature` | `0` | Deterministic tool routing |
| `streaming` | `True` | Required for Chainlit integration |
| `max_iterations` | default (25) | Max ReAct loops before stopping |

## Example Usage

```python
# Day 3 demo questions — the agent routes each correctly:

# → supabase_execute_sql
ask("Quantos pedidos foram feitos por pix?")
ask("Top 5 produtos por faturamento")
ask("Distribuicao de clientes por segmento")

# → qdrant_semantic_search
ask("O que os clientes falam sobre qualidade?")
ask("Reviews negativos sobre frete")
ask("Clientes satisfeitos com o produto")
```

## See Also

- [LangGraph Routing](../patterns/langgraph-routing.md)
- [Tools](../concepts/tools.md)
- [Supabase Ledger Queries](../../supabase/patterns/shopagent-ledger-queries.md)
- [Chainlit Integration](../../chainlit/patterns/langchain-integration.md)



# OBJECTIVE

Create Pydantic models for ShopAgent