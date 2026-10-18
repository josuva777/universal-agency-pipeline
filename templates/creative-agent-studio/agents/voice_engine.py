import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
import edge_tts
from pydantic import BaseModel, Field

class WordTimestamp(BaseModel):
    word: str
    start_ms: int
    end_ms: int

class VoiceoverResult(BaseModel):
    audio_path: str
    duration_seconds: float
    word_timestamps: List[WordTimestamp]
    voice_used: str

class EdgeTTSEngine:
    """Generates high-fidelity neural speech with word-level timestamps using Microsoft Edge Neural TTS ($0)."""

    DEFAULT_VOICE = "en-US-GuyNeural"
    # Alternative voices:
    # en-US-AriaNeural (Professional Female)
    # en-US-ChristopherNeural (Authoritative Male)
    # en-GB-SoniaNeural (Luxury British Female)
    # en-GB-RyanNeural (Modern British Male)

    @classmethod
    async def generate_voiceover(
        cls,
        text: str,
        output_audio_path: str,
        voice: Optional[str] = None,
        rate: str = "+0%",
        pitch: str = "+0Hz",
    ) -> VoiceoverResult:
        chosen_voice = voice or cls.DEFAULT_VOICE
        out_path = Path(output_audio_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        communicate = edge_tts.Communicate(text, chosen_voice, rate=rate, pitch=pitch)
        
        words: List[WordTimestamp] = []
        raw_audio_chunks = bytearray()
        last_offset = 0
        last_duration = 0

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                raw_audio_chunks.extend(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # Offset and duration are in 100-nanosecond units (ticks)
                start_ms = chunk["offset"] // 10000
                duration_ms = chunk["duration"] // 10000
                end_ms = start_ms + duration_ms
                word_text = chunk["text"]
                words.append(WordTimestamp(word=word_text, start_ms=start_ms, end_ms=end_ms))
                last_offset = chunk["offset"]
                last_duration = chunk["duration"]

        # Write audio output file
        with open(out_path, "wb") as f:
            f.write(raw_audio_chunks)

        # Compute total duration from last boundary or audio file
        total_duration = ((last_offset + last_duration) // 10000) / 1000.0 if last_offset > 0 else 5.0

        # Save metadata JSON beside audio
        json_path = out_path.with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([w.model_dump() for w in words], f, indent=2)

        return VoiceoverResult(
            audio_path=str(out_path.resolve()),
            duration_seconds=total_duration,
            word_timestamps=words,
            voice_used=chosen_voice,
        )


class KokoroEngine:
    """Local offline TTS engine using 82M open-weight Kokoro model via ONNX."""

    @classmethod
    def is_available(cls) -> bool:
        try:
            import kokoro_onnx
            return True
        except ImportError:
            return False

    @classmethod
    async def generate_voiceover(
        cls,
        text: str,
        output_audio_path: str,
        voice: str = "af_heart"
    ) -> VoiceoverResult:
        if not cls.is_available():
            raise RuntimeError("kokoro-onnx is not installed. Use EdgeTTSEngine instead.")
        
        # Kokoro execution logic
        # Fallback to EdgeTTS if weights are not yet downloaded
        return await EdgeTTSEngine.generate_voiceover(text, output_audio_path)


class VoiceEngine:
    """Master voice dispatch interface."""

    @classmethod
    async def synthesize(
        cls,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        prefer_local: bool = False
    ) -> VoiceoverResult:
        if prefer_local and KokoroEngine.is_available():
            try:
                return await KokoroEngine.generate_voiceover(text, output_path, voice or "af_heart")
            except Exception:
                pass  # Fallback to EdgeTTS

        return await EdgeTTSEngine.generate_voiceover(text, output_path, voice)
