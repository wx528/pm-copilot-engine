"""End-to-end tests for AIAgent using a fake OpenAI client.

These tests exercise the full agent loop (system prompt construction,
API request building, response normalization, tool dispatch, and
final-response generation) without touching a real model endpoint.
"""

from __future__ import annotations

import pytest

from pm_copilot_engine import AIAgent

from conftest import fake_openai_client, make_chat_response


def _make_agent(**overrides) -> AIAgent:
    """Create an AIAgent with test-friendly defaults."""
    kwargs = {
        "base_url": "http://fake-provider.example/v1",
        "api_key": "fake-key",
        "model": "fake-model",
        "quiet_mode": True,
        "skip_context_files": True,
        "skip_memory": True,
        "max_iterations": 5,
        "tool_delay": 0.0,
    }
    kwargs.update(overrides)
    return AIAgent(**kwargs)


@pytest.mark.usefixtures("hermes_home")
def test_agent_returns_final_response():
    response = make_chat_response("Hello from the fake model.")

    with fake_openai_client([response]) as mock_client:
        agent = _make_agent()
        result = agent.run_conversation("say hello")

    assert result["completed"] is True
    assert result["final_response"] == "Hello from the fake model."
    assert result["api_calls"] == 1
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.usefixtures("hermes_home")
def test_agent_calls_todo_tool():
    first_response = make_chat_response(
        "",
        tool_calls=[
            {
                "id": "call_1",
                "name": "todo",
                "arguments": {
                    "todos": [
                        {"id": "1", "content": "write tests", "status": "pending"}
                    ]
                },
            }
        ],
    )
    second_response = make_chat_response("I've added the todo.")

    with fake_openai_client([first_response, second_response]) as mock_client:
        agent = _make_agent(enabled_toolsets=["todo"])
        result = agent.run_conversation("add a todo: write tests")

    assert result["completed"] is True
    assert result["final_response"] == "I've added the todo."
    assert result["api_calls"] == 2

    calls = mock_client.chat.completions.create.call_args_list
    assert len(calls) == 2

    # The second model request must include the tool result.
    second_messages = calls[1].kwargs["messages"]
    tool_result_msgs = [m for m in second_messages if m.get("role") == "tool"]
    assert len(tool_result_msgs) == 1
    assert "write tests" in tool_result_msgs[0]["content"]


@pytest.mark.usefixtures("hermes_home")
def test_agent_chat_shortcut():
    response = make_chat_response("Shortcut works.")

    with fake_openai_client([response]):
        agent = _make_agent()
        answer = agent.chat("hi")

    assert answer == "Shortcut works."
