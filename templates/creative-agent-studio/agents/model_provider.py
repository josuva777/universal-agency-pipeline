"""Centralized AI Model Provider Architecture with Multi-Model Failover,
Exponential Backoff Retries, and Rate-Limit Handling (2026 Standards).
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

# Modern 2026 Model Registry
DEFAULT_MODELS = {
    "gemini": ModelConfig(provider="gemini", model_id="gemini-2.5-flash", timeout_seconds=12.0),
    "groq": ModelConfig(provider="groq", model_id="llama-3.3-70b-versatile", timeout_seconds=10.0),
    "openai": ModelConfig(provider="openai", model_id="gpt-4o-mini", timeout_seconds=10.0),
    "anthropic": ModelConfig(provider="anthropic", model_id="claude-3-5-sonnet-20241022", timeout_seconds=15.0),
}

class CentralizedModelProvider:
    """Manages multi-provider execution with prioritized failover and rate-limit backoff."""

    def __init__(self, priority_order: Optional[List[str]] = None):
        self.priority_order = priority_order or ["gemini", "groq", "openai"]

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
                        # Rate limited: exponential backoff
                        await asyncio.sleep(1.5 * (attempt + 1))
                        continue
                    else:
                        break
            except Exception:
                if attempt == config.max_retries:
                    break
                await asyncio.sleep(1.0)
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
                        await asyncio.sleep(1.5 * (attempt + 1))
                        continue
                    else:
                        break
            except Exception:
                if attempt == config.max_retries:
                    break
                await asyncio.sleep(1.0)
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
                        await asyncio.sleep(1.5 * (attempt + 1))
                        continue
                    else:
                        break
            except Exception:
                if attempt == config.max_retries:
                    break
                await asyncio.sleep(1.0)
        return None

    async def generate_json(self, prompt: str) -> tuple[Optional[Dict[str, Any]], str]:
        """Iterates through priority models with automatic failover.
        Returns: (parsed_json_dict, provider_name_used)
        """
        for provider_name in self.priority_order:
            config = DEFAULT_MODELS.get(provider_name)
            if not config:
                continue

            raw_text = None
            if provider_name == "gemini":
                raw_text = await self._call_gemini(prompt, config)
            elif provider_name == "groq":
                raw_text = await self._call_groq(prompt, config)
            elif provider_name == "openai":
                raw_text = await self._call_openai(prompt, config)

            if raw_text:
                try:
                    parsed = json.loads(raw_text)
                    return parsed, f"{provider_name} ({config.model_id})"
                except json.JSONDecodeError:
                    continue

        return None, "offline_fallback"
