"""Automated Unit Tests for Centralized Model Provider Architecture."""
import sys
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "templates" / "creative-agent-studio"))

from agents.model_provider import CentralizedModelProvider, DEFAULT_MODELS, ModelConfig, get_default_models

def test_model_registry_defaults():
    assert "gemini" in DEFAULT_MODELS
    assert "groq" in DEFAULT_MODELS
    assert "anthropic" in DEFAULT_MODELS
    assert "openai" in DEFAULT_MODELS
    assert DEFAULT_MODELS["gemini"].model_id == "gemini-2.0-flash"
    assert DEFAULT_MODELS["groq"].model_id == "llama-3.3-70b-versatile"
    assert DEFAULT_MODELS["anthropic"].model_id == "claude-3-5-sonnet-latest"
    assert DEFAULT_MODELS["openai"].model_id == "gpt-4o-mini"

def test_model_registry_env_overrides(monkeypatch):
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-pro")
    monkeypatch.setenv("ANTHROPIC_MODEL", "claude-3-7-sonnet")
    custom_registry = get_default_models()
    assert custom_registry["gemini"].model_id == "gemini-2.5-pro"
    assert custom_registry["anthropic"].model_id == "claude-3-7-sonnet"

def test_custom_model_config_in_provider():
    custom_cfg = {"gemini": ModelConfig(provider="gemini", model_id="custom-fast-gemini", timeout_seconds=5.0)}
    provider = CentralizedModelProvider(models=custom_cfg)
    assert provider.models["gemini"].model_id == "custom-fast-gemini"
    assert provider.models["gemini"].timeout_seconds == 5.0

@pytest.mark.asyncio
async def test_offline_fallback_when_no_keys_present(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    provider = CentralizedModelProvider()
    parsed, source = await provider.generate_json("Generate commercial script")
    assert parsed is None
    assert source == "offline_fallback"
