"""Smoke tests for pm-copilot-engine.

These tests verify that the public API can be imported and basic
structures are present after packaging.
"""

import pm_copilot_engine
from pm_copilot_engine import AIAgent, registry, TOOLSETS


def test_version_present():
    assert isinstance(pm_copilot_engine.__version__, str)
    parts = pm_copilot_engine.__version__.split(".")
    assert len(parts) >= 2


def test_public_api_importable():
    assert callable(AIAgent)
    assert registry is not None
    assert isinstance(TOOLSETS, dict)
    assert len(TOOLSETS) > 0


def test_tool_registry_has_entries():
    names = registry.get_registered_toolset_names()
    assert len(names) > 0
