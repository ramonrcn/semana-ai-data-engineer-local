"""Shared LLM configuration for Anthropic or OpenAI-compatible providers."""

from __future__ import annotations

import os
from typing import Any

import anthropic
from llama_index.core import Settings
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from openai import OpenAI


def get_llm_provider() -> str:
    return os.environ.get("LLM_PROVIDER", "openai_compatible").strip().lower()


def get_llm_model() -> str:
    provider = get_llm_provider()
    if provider == "anthropic":
        return os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    return os.environ.get("OPENAI_MODEL", "local-model")


def get_openai_client() -> OpenAI:
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "lm-studio"),
        base_url=os.environ.get("OPENAI_BASE_URL", "http://localhost:1234/v1"),
    )


def get_anthropic_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )


def get_llamaindex_llm() -> Any:
    provider = get_llm_provider()
    if provider == "anthropic":
        return Anthropic(model=get_llm_model())

    return LlamaOpenAI(
        model=get_llm_model(),
        api_key=os.environ.get("OPENAI_API_KEY", "lm-studio"),
        api_base=os.environ.get("OPENAI_BASE_URL", "http://localhost:1234/v1"),
    )


def configure_llamaindex() -> None:
    Settings.llm = get_llamaindex_llm()
    Settings.embed_model = FastEmbedEmbedding(
        model_name=os.environ.get("EMBED_MODEL", "BAAI/bge-base-en-v1.5")
    )
