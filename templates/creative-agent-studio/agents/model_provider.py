"""Centralized AI Model Provider Architecture with Multi-Model Failover,
True Exponential Backoff, and Full Anthropic/Gemini/OpenAI/Groq Dispatch (2026 Standards).
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional
import httpx
from pydantic import BaseModel, Field

class ModelConfig(BaseModel):
    provider: str
    model_id: str
    timeout_seconds: float = 12.0
    max_retries: int = 2

# Modern Verified 2026 Model Registry with Dynamic Env Overrides
def get_default_models(overrides: Optional[Dict[str, ModelConfig]] = None) -> Dict[str, ModelConfig]:
    """Generates the active model registry with dynamic environment variable overrides."""
    registry = {
        "gemini": ModelConfig(
            provider="gemini",
            model_id=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            timeout_seconds=float(os.getenv("GEMINI_TIMEOUT", "12.0")),
        ),
        "groq": ModelConfig(
            provider="groq",
            model_id=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            timeout_seconds=float(os.getenv("GROQ_TIMEOUT", "10.0")),
        ),
        "anthropic": ModelConfig(
            provider="anthropic",
            model_id=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest"),
            timeout_seconds=float(os.getenv("ANTHROPIC_TIMEOUT", "15.0")),
        ),
        "openai": ModelConfig(
            provider="openai",
            model_id=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            timeout_seconds=float(os.getenv("OPENAI_TIMEOUT", "10.0")),
        ),
    }
    if overrides:
        registry.update(overrides)
    return registry

DEFAULT_MODELS = get_default_models()

class CentralizedModelProvider:
    """Manages multi-provider execution with prioritized failover and exponential backoff."""

    def __init__(
        self,
        priority_order: Optional[List[str]] = None,
        models: Optional[Dict[str, ModelConfig]] = None,
    ):
        self.priority_order = priority_order or ["gemini", "groq", "anthropic", "openai"]
        self.models = get_default_models(models)

    def check_provider_health(self, provider_name: str) -> Dict[str, Any]:
        """Audits credential availability and model configuration for a provider."""
        key_map = {
            "gemini": "GEMINI_API_KEY",
            "groq": "GROQ_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
        }
        env_var = key_map.get(provider_name)
        if not env_var:
            return {"provider": provider_name, "status": "unsupported", "configured": False}

        key = os.getenv(env_var)
        configured = bool(key and not key.startswith("your_"))
        config = self.models.get(provider_name)
        return {
            "provider": provider_name,
            "model_id": config.model_id if config else "unknown",
            "configured": configured,
            "status": "ready" if configured else "missing_api_key",
        }

    async def _call_gemini(self, prompt: str, config: ModelConfig) -> Optional[str]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key.startswith("your_"):
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.model_id}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }

        for attempt in range(config.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
                    res = await client.post(url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                    elif res.status_code == 429:
                        # True exponential backoff
                        await asyncio.sleep(1.5 * (2 ** attempt))
                        continue
                    else:
                        break
            except Exception:
                if attempt == config.max_retries:
                    break
                await asyncio.sleep(1.0 * (2 ** attempt))
        return None

    async def _call_groq(self, prompt: str, config: ModelConfig) -> Optional[str]:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key.startswith("your_"):
            return None

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": config.model_id,
            "messages": [
                {"role": "system", "content": "You are an elite creative director. Respond with pure JSON only."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        for attempt in range(config.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
                    res = await client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        return res.json()["choices"][0]["message"]["content"]
                    elif res.status_code == 429:
                        await asyncio.sleep(1.5 * (2 ** attempt))
                        continue
                    else:
                        break
            except Exception:
                if attempt == config.max_retries:
                    break
                await asyncio.sleep(1.0 * (2 ** attempt))
        return None

    async def _call_anthropic(self, prompt: str, config: ModelConfig) -> Optional[str]:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key.startswith("your_"):
            return None

        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": config.model_id,
            "max_tokens": 1500,
            "messages": [{"role": "user", "content": prompt}],
            "system": "You are an elite creative director. Respond with pure JSON only."
        }

        for attempt in range(config.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
                    res = await client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        return data["content"][0]["text"]
                    elif res.status_code == 429:
                        await asyncio.sleep(1.5 * (2 ** attempt))
                        continue
                    else:
                        break
            except Exception:
                if attempt == config.max_retries:
                    break
                await asyncio.sleep(1.0 * (2 ** attempt))
        return None

    async def _call_openai(self, prompt: str, config: ModelConfig) -> Optional[str]:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("your_"):
            return None

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {
            "model": config.model_id,
            "messages": [
                {"role": "system", "content": "You are an elite creative director. Respond with pure JSON only."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        for attempt in range(config.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=config.timeout_seconds) as client:
                    res = await client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        return res.json()["choices"][0]["message"]["content"]
                    elif res.status_code == 429:
                        await asyncio.sleep(1.5 * (2 ** attempt))
                        continue
                    else:
                        break
            except Exception:
                if attempt == config.max_retries:
                    break
                await asyncio.sleep(1.0 * (2 ** attempt))
        return None

    async def generate_json(self, prompt: str) -> tuple[Optional[Dict[str, Any]], str]:
        """Iterates through priority models with automatic failover and schema validation.
        Returns: (parsed_json_dict, provider_name_used)
        """
        for provider_name in self.priority_order:
            config = self.models.get(provider_name) or DEFAULT_MODELS.get(provider_name)
            if not config:
                continue

            raw_text = None
            if provider_name == "gemini":
                raw_text = await self._call_gemini(prompt, config)
            elif provider_name == "groq":
                raw_text = await self._call_groq(prompt, config)
            elif provider_name == "anthropic":
                raw_text = await self._call_anthropic(prompt, config)
            elif provider_name == "openai":
                raw_text = await self._call_openai(prompt, config)

            if raw_text:
                try:
                    parsed = json.loads(raw_text)
                    return parsed, f"{provider_name} ({config.model_id})"
                except json.JSONDecodeError:
                    continue

        return None, "offline_fallback"
