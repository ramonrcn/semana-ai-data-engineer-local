# 🚀 Local AI Agent for Data Engineering (Deterministic Architecture)

## 🧠 Overview

This project implements a **fully local AI agent** designed to replicate the behavior of tools like Codex/Claude Code — but with **deterministic execution, full system control, and zero dependency on paid APIs**.

Instead of relying on prompt engineering alone, this system is built with **software engineering principles**:

- Separation of responsibilities
- Deterministic execution
- Tool-driven architecture 
- Observability and traceability (WIP)

- OBS: You can find the original readme file at /semana-ai-data-engineer-main

---

## ⚙️ Architecture

```
User Input
   ↓
Agent (decision layer)
   ↓
MCP Server (execution layer)
   ↓
Tools (SQL / Code / Domain)
   ↓
PostgreSQL / Output
```

### Key Principle

> The LLM does NOT execute. It orchestrates.

---

## 🧱 Core Components

### 🧠 Agent (Continue + Local LLM)
- Responsible for **decision making only**
- Routes requests to appropriate tools
- No direct execution

### 🔌 MCP Server (Custom)
- Central execution engine
- Handles:
  - SQL execution
  - Domain normalization
  - Code generation

### 🛠 Tools
- `run_sql` → Executes validated queries
- `schema_reader` → Reads database structure
- `generator` → Transforms structured data into code

### 🗄 Database
- PostgreSQL as **single source of truth**
- No hallucinated schema

---

## 🔥 Key Design Decisions

### 1. Determinism over intelligence
- Temperature = 0
- Structured outputs
- Minimal ambiguity

### 2. Prompts are contracts
- Prompts are NOT modified
- System adapts via architecture, not prompt hacking

### 3. Parser over heuristics
- SQL is parsed and normalized before execution
- Avoids LLM guessing

### 4. Domain normalization layer
- Maps raw SQL → domain concepts
- Ensures consistency with real system

---

## ⚠️ Problems Solved

- Agent ignoring tools
- LLM hallucinating schema
- Non-deterministic outputs
- Code generation inconsistencies
- Database vs code mismatch

---

## 📈 Current Status

- [x] Local agent working
- [x] MCP server orchestrating execution
- [x] Real database queries
- [x] SQL parser implemented
- [x] Domain normalization layer
- [ ] Execution tracing (planned)
- [ ] Automated evals (planned)

---

## 🔍 Example Flow

**Input:**
```
List active credit cards
```

**Execution:**
```
Agent → selects run_sql
→ MCP validates SQL
→ Query executed in Postgres
→ Result normalized
→ Output returned
```

---

## 🧪 Roadmap

- [ ] Full execution trace logs
- [ ] Automated evaluation suite
- [ ] Specialyzed agents for each kind of task
- [ ] Deterministic tool router
- [ ] Generator constraints hardening

---

## 💻 Hardware Requirements

- GPU: RTX 3060 (tested)
- RAM: 16GB
- LLM: qwen2.5-coder:7b

---

## 🚀 Why This Project Matters

Most AI projects:
- Depend on APIs
- Rely on prompt engineering
- Are non-deterministic

This project:
- Runs **fully local**
- Is **architecturally controlled**
- Treats LLM as a **component, not a solution**

---

## 📌 Final Note

This is not a demo.

This is a **system design exercise applied to AI engineering** — focused on reliability, control, and real-world applicability.

---

## 🤝 Author

Ramon N.

---

## ⭐ If this project resonates with you

Give it a star, fork it, or reach out — always open to deep technical discussions.

