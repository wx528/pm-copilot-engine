"""Integration tests that hit real model endpoints.

These tests exercise the agent against a real LLM API. They default to the
official OpenAI endpoint, but can be pointed at any OpenAI-compatible API
(MiniMax, Moonshot, DeepSeek, OpenRouter, etc.) via environment variables.

Run locally:

    # Windows PowerShell
    $env:PMCE_API_KEY = "sk-..."
    $env:PMCE_BASE_URL = "https://api.openai.com/v1"   # or your provider
    $env:PMCE_MODEL = "gpt-4o-mini"                    # or "minimax-m3", etc.
    uv run pytest tests/test_agent_integration.py -v

    # bash / WSL
    export PMCE_API_KEY=sk-...
    export PMCE_BASE_URL=https://api.openai.com/v1
    export PMCE_MODEL=gpt-4o-mini
    uv run pytest tests/test_agent_integration.py -v

Tests are marked ``integration`` and are excluded from the default pytest run
by ``addopts = "-m 'not integration'"`` in ``pyproject.toml``.  They skip
automatically when ``PMCE_API_KEY`` is not set.
"""

from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv

from pm_copilot_engine import AIAgent


# Allow local `.env` to supply PMCE_* variables for integration tests.
load_dotenv()


pytestmark = pytest.mark.integration


def _env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name, default)


@pytest.fixture
def real_agent(hermes_home: str) -> AIAgent:
    """Create an AIAgent wired to a real LLM API.

    Configurable via environment variables:

    - ``PMCE_API_KEY``   required
    - ``PMCE_BASE_URL``  default: https://api.openai.com/v1
    - ``PMCE_MODEL``     default: gpt-4o-mini
    - ``PMCE_PROVIDER``  optional hint (openai, minimax, ...)
    """
    api_key = _env("PMCE_API_KEY")
    if not api_key:
        pytest.skip("PMCE_API_KEY not set")

    base_url = _env("PMCE_BASE_URL", "https://api.openai.com/v1")
    model = _env("PMCE_MODEL", "gpt-4o-mini")
    provider = _env("PMCE_PROVIDER")

    kwargs: dict = {
        "base_url": base_url,
        "api_key": api_key,
        "model": model,
        "quiet_mode": True,
        "skip_context_files": True,
        "skip_memory": True,
        "max_iterations": 5,
        "tool_delay": 0.0,
    }
    if provider:
        kwargs["provider"] = provider

    return AIAgent(**kwargs)


def test_real_model_responds(real_agent: AIAgent) -> None:
    """The model should follow a simple instruction and return a response."""
    result = real_agent.run_conversation("Say exactly the word 'pong'.")

    assert result["completed"] is True
    assert result["final_response"]
    assert "pong" in result["final_response"].lower()


def test_real_model_uses_todo_tool(real_agent: AIAgent) -> None:
    """The model should use the todo tool when asked to track a task."""
    real_agent.enabled_toolsets = ["todo"]

    result = real_agent.run_conversation(
        "Add a todo item with id 't1' and content 'buy milk'. "
        "Then tell me the todo was added."
    )

    assert result["completed"] is True
    assert "buy milk" in result["final_response"].lower()
