"""Kilo Code provider profile."""

from pm_copilot_engine.providers import register_provider
from pm_copilot_engine.providers.base import ProviderProfile

kilocode = ProviderProfile(
    name="kilocode",
    aliases=("kilo-code", "kilo", "kilo-gateway"),
    env_vars=("KILOCODE_API_KEY",),
    base_url="https://api.kilo.ai/api/gateway",
    default_aux_model="google/gemini-3-flash-preview",
)

register_provider(kilocode)
