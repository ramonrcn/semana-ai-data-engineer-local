# Local AI Agent with MCP Orchestration

This project is an implementation of a fully local AI agent capable of executing real tasks using tool orchestration — inspired by systems like Codex and Claude Code, but without relying on paid APIs.

## Overview

Instead of relying on LLMs to generate answers, this project focuses on building a deterministic system where:

- The LLM acts as a **decision layer**
- A custom MCP server handles **execution**
- Tools provide **real-world actions** (database, files, etc.)

## Architecture


User Prompt
↓
Agent (Continue)
↓
MCP Server (custom)
↓
Tools (Postgres, File System, Generators)
↓
Structured Output


## Tech Stack

- **Ollama** — local LLM execution
- **Continue (VSCode)** — agent interface
- **Custom MCP Server** — orchestration layer
- **PostgreSQL** — structured data (ledger)
- **Python** — core implementation

## Key Concepts

### 1. LLM as Orchestrator

The model does not execute logic.  
It decides which tool to use.

### 2. MCP as Execution Layer

All real operations are handled by MCP:

- SQL queries
- File reading/writing
- Code generation

### 3. Deterministic Behavior

The system is designed to avoid hallucinations:

- No direct database access via LLM
- No code generation without constraints
- Strict tool routing

### 4. Parser-Based Code Generation

Instead of relying on LLM-generated code:

- SQL schema is parsed
- Constraints are extracted
- Domain normalization is applied
- Code is generated deterministically

## Features

- Local AI agent (no API costs)
- Real database querying via tools
- Schema-aware analysis
- Structured outputs
- Deterministic code generation
- Domain normalization (e.g., `credit_card`, `processing`)

## Design Principles

- Do not modify prompts — adapt the system
- Separate decision from execution
- Prefer determinism over model creativity
- Treat LLM as a component, not the system

## Current Status

- Agent fully functional locally
- MCP server operational
- SQL execution working
- Schema parsing implemented
- Domain normalization in place

## Next Steps

- Byte-level reproducibility for generated code
- Automatic validation against reference implementations
- Multi-step planner/executor flow
- Expansion to full multi-agent system

## Key Insight

> LLM alone is just a smart interface.  
> LLM + tools is a real system.

### You can find the original readme file inside /...-main