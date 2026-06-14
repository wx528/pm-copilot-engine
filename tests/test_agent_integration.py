"""Integration tests that hit real model endpoints.

Run locally with a real API key:

    # Windows PowerShell
    $env:OPENAI_API_KEY = "sk-..."
    uv run pytest tests/test_agent_integration.py -v

    # bash / WSL
    export OPENAI_API_KEY=sk-...
    uv run pytest tests/test_agent_integration.py -v

These tests are marked ``integration`` and are excluded from the default
pytest run by ``addopts = "-m 'not integration'"`` in ``pyproject.toml``.
"""

from __future__ import annotations

import os

import pytest

from pm_copilot_engine import AIAgent


pytestmark = pytest.mark.integration


def _api_key() -> str | None:
    return os.environ.get("OPENAI_API_KEY")


@pytest.fixture
def openai_agent(hermes_home: str) -> AIAgent:
    """Create an AIAgent wired to the real OpenAI API.

    Skips the test when ``OPENAI_API_KEY`` is not available.
    """
    key = _api_key()
    if not key:
        pytest.skip("OPENAI_API_KEY not set")

    return AIAgent(
        base_url="https://api.openai.com/v1",
        api_key=key,
        model="gpt-4o-mini",
        quiet_mode=True,
        skip_context_files=True,
        skip_memory=True,
        max_iterations=5,
        tool_delay=0.0,
    )


def test_real_model_responds(openai_agent: AIAgent) -> None:
    result = openai_agent.run_conversation("Say exactly the word 'pong'.")

    assert result["completed"] is True
    assert result["final_response"]
    assert "pong" in result["final_response"].lower()


def test_real_model_uses_todo_tool(openai_agent: AIAgent) -> None:
    """Ask the model to use the todo tool and verify the result is surfaced."""
    openai_agent.enabled_toolsets = ["todo"]

    result = openai_agent.run_conversation(
        "Add a todo item with id 't1' and content 'buy milk'. "
        "Then tell me the todo was added."
    )

    assert result["completed"] is True
    assert "buy milk" in result["final_response"].lower()
