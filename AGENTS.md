# pm-copilot-engine — Development Guide

Instructions for AI coding assistants and developers working on the `pm-copilot-engine` package.

This repository is a fork of [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent). The goal is to ship the Hermes agent **core** as a reusable Python library under the `pm_copilot_engine` namespace, not as a full end-user application.

## Project structure

- `pm_copilot_engine/` — The public package.
  - `run_agent.py` — `AIAgent` class.
  - `model_tools.py`, `toolsets.py` — Tool orchestration.
  - `tools/`, `agent/`, `providers/` — Core tool/agent/provider implementations.
  - `_internal/hermes_cli/` — Internalized Hermes config/auth/helpers. Do not import directly from downstream code; it is an implementation detail.
- `plugins/` — Bundled providers (browser, web search, memory) required by core tools.
- `cron/` — Cron helpers required by core tools.
- `pyproject.toml` — Package metadata and dependencies.

## Design principles

1. **Public API is small.** Downstream code should import only `AIAgent`, `registry`, and `TOOLSETS` from `pm_copilot_engine`.
2. **Keep the core narrow.** New capabilities should prefer plugins, skills, or downstream PM-system code over changes to `pm_copilot_engine` core modules.
3. **Do not leak `pm_copilot_engine._internal` into public docs or examples.** It exists only because `AIAgent` still depends on Hermes config/auth internals.
4. **Preserve prompt caching and message-role alternation** when touching the conversation loop.

## Build / test / publish

```bash
# Editable install
pip install -e .

# Smoke test
python -c "from pm_copilot_engine import AIAgent, registry, TOOLSETS; print('OK')"

# Build
python -m build

# Check
twine check dist/*

# Publish to TestPyPI
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*
```

## When modifying imports

If you move or rename modules, update both:
- Absolute imports inside `pm_copilot_engine/`, `plugins/`, and `cron/`.
- `pm_copilot_engine/tools/registry.py` `discover_builtin_tools()` module prefix.

## License

MIT — see [LICENSE](LICENSE).
