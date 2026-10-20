"""Automated Unit Tests for Centralized Model Provider Architecture."""
import sys
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "templates" / "creative-agent-studio"))

from unittest.mock import AsyncMock, patch
from agents.model_provider import CentralizedModelProvider, DEFAULT_MODELS, ModelConfig, get_default_models

def test_model_registry_defaults():
    assert "gemini" in DEFAULT_MODELS
    assert "groq" in DEFAULT_MODELS
    assert "anthropic" in DEFAULT_MODELS
    assert "openai" in DEFAULT_MODELS
    assert DEFAULT_MODELS["gemini"].model_id == "gemini-2.5-flash"
    assert DEFAULT_MODELS["groq"].model_id == "llama-3.3-70b-versatile"
    assert DEFAULT_MODELS["anthropic"].model_id == "claude-3-5-sonnet-latest"
    assert DEFAULT_MODELS["openai"].model_id == "gpt-4o-mini"

def test_check_provider_health(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-proj-placeholder-test-1234567890abcdef")
    provider = CentralizedModelProvider()

    health_gemini = provider.check_provider_health("gemini")
    assert health_gemini["configured"] is False
    assert health_gemini["status"] == "missing_api_key"

    health_openai = provider.check_provider_health("openai")
    assert health_openai["configured"] is True
    assert health_openai["status"] == "ready"

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
async def test_multi_model_failover_chain():
    provider = CentralizedModelProvider(priority_order=["gemini", "groq"])

    # Simulate Gemini failing (rate limit / outage) and Groq succeeding
    with patch.object(provider, "_call_gemini", new_callable=AsyncMock) as mock_gemini, \
         patch.object(provider, "_call_groq", new_callable=AsyncMock) as mock_groq:
        mock_gemini.return_value = None
        mock_groq.return_value = '{"project_title": "Apex Commercial", "status": "ok"}'

        result, provider_used = await provider.generate_json("Generate script")
        assert result is not None
        assert result["project_title"] == "Apex Commercial"
        assert "groq" in provider_used
        mock_gemini.assert_awaited_once()
        mock_groq.assert_awaited_once()

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
