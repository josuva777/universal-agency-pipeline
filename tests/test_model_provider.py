"""Automated Unit Tests for Centralized Model Provider Architecture."""
import sys
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "templates" / "creative-agent-studio"))

from agents.model_provider import CentralizedModelProvider, DEFAULT_MODELS, ModelConfig

def test_model_registry_defaults():
    assert "gemini" in DEFAULT_MODELS
    assert "groq" in DEFAULT_MODELS
    assert "anthropic" in DEFAULT_MODELS
    assert "openai" in DEFAULT_MODELS
    assert DEFAULT_MODELS["gemini"].model_id == "gemini-2.0-flash"
    assert DEFAULT_MODELS["groq"].model_id == "llama-3.3-70b-versatile"
    assert DEFAULT_MODELS["anthropic"].model_id == "claude-3-5-sonnet-latest"
    assert DEFAULT_MODELS["openai"].model_id == "gpt-4o-mini"

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
