"""Shared fixtures for pm-copilot-engine tests."""

from __future__ import annotations

import contextlib
import json
import os
from types import SimpleNamespace
from typing import Any, Iterator
from unittest.mock import Mock, patch

import pytest


def make_chat_response(
    content: str = "",
    tool_calls: list[dict[str, Any]] | None = None,
    finish_reason: str | None = None,
) -> SimpleNamespace:
    """Build a fake OpenAI chat completion response."""
    tool_call_objects = None
    if tool_calls:
        tool_call_objects = [
            SimpleNamespace(
                id=tc.get("id", f"call_{i}"),
                function=SimpleNamespace(
                    name=tc["name"],
                    arguments=json.dumps(tc.get("arguments", {})),
                ),
            )
            for i, tc in enumerate(tool_calls)
        ]

    message = SimpleNamespace(
        content=content or None,
        tool_calls=tool_call_objects,
    )
    choice = SimpleNamespace(
        message=message,
        finish_reason=finish_reason or ("tool_calls" if tool_calls else "stop"),
    )
    usage = SimpleNamespace(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
    )
    return SimpleNamespace(choices=[choice], usage=usage, model="fake-model")


@pytest.fixture
def hermes_home(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> str:
    """Provide an isolated HERMES_HOME directory for each test."""
    home = str(tmp_path / "hermes_home")
    os.makedirs(home, exist_ok=True)
    monkeypatch.setenv("HERMES_HOME", home)
    return home


@pytest.fixture
def patched_openai_client() -> Iterator[Mock]:
    """Patch the OpenAI client factory used by AIAgent.

    Yields the mock *client instance* whose
    ``chat.completions.create`` return value/side_effect can be configured
    by the test before instantiating AIAgent.
    """
    with patch("pm_copilot_engine.run_agent.OpenAI") as MockOpenAI:
        mock_client = Mock()
        MockOpenAI.return_value = mock_client
        yield mock_client


@contextlib.contextmanager
def fake_openai_client(responses: list[Any] | Any) -> Iterator[Mock]:
    """Context-manager helper for tests that don't want a fixture.

    ``responses`` may be a single response or a list of responses used as
    ``side_effect`` for ``chat.completions.create``.
    """
    responses_list = responses if isinstance(responses, list) else [responses]
    with patch("pm_copilot_engine.run_agent.OpenAI") as MockOpenAI:
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = responses_list
        MockOpenAI.return_value = mock_client
        yield mock_client
