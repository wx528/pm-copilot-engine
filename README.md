# pm-copilot-engine

AI Agent Engine for Project Management — a focused fork of [Hermes](https://github.com/NousResearch/hermes-agent) by NousResearch, packaged as a reusable Python library.

Repository: https://github.com/wx528/pm-copilot-engine

## What it is

`pm-copilot-engine` exposes the core agent runtime from Hermes as a pip-installable package. It is intended to be embedded in project-management systems that need an LLM agent with tool calling, file/terminal/browser tools, memory, and skill management — without shipping the full Hermes CLI, gateway, TUI, or web dashboard.

## Install

```bash
pip install pm-copilot-engine
```

## Quick start

```python
from pm_copilot_engine import AIAgent, registry, TOOLSETS

agent = AIAgent(
    base_url="https://api.openai.com/v1",
    api_key="sk-...",
    model="gpt-4o",
)

response = agent.chat("Summarize the project status from ./README.md")
print(response)
```

## Package layout

```text
pm_copilot_engine/          # Public package
    __init__.py             # Exports AIAgent, registry, TOOLSETS
    run_agent.py            # AIAgent class
    model_tools.py          # Tool dispatch
    toolsets.py             # Built-in toolsets
    tools/                  # Tool implementations
    agent/                  # Agent internals
    providers/              # Provider adapters
    _internal/hermes_cli/   # Internalized config/auth/helpers from Hermes
plugins/                    # Browser/web/memory providers required by core tools
cron/                       # Cron helpers required by core tools
```

## Differences from upstream Hermes

- Repackaged under `pm_copilot_engine.*` namespace.
- Removed CLI entry points (`hermes`, `hermes-agent`, `hermes-acp`).
- Removed gateway, TUI, web dashboard, Docker, ACP adapter, and optional skills.
- Kept the internal Hermes config/auth layer as `pm_copilot_engine._internal.hermes_cli`.
- Preserved bundled browser/web/memory/cron providers needed by the core tool registry.

## License

MIT — see [LICENSE](LICENSE).
