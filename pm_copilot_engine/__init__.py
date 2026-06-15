"""pm-copilot-engine: AI Agent Engine for Project Management.

Forked from Hermes by NousResearch, tailored for PM Copilot.
"""

from pm_copilot_engine.run_agent import AIAgent
from pm_copilot_engine.tools.registry import registry
from pm_copilot_engine.toolsets import TOOLSETS

__version__ = "0.2.0"
__all__ = ["AIAgent", "registry", "TOOLSETS"]
