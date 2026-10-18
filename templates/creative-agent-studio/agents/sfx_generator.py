import math
import wave
import struct
from pathlib import Path
from typing import Dict

class ProceduralSFXGenerator:
    """Generates broadcast-grade acoustic sound effects (risers, whooshes, sub-drops, tactile clicks)

    purely with Python math & wave - zero dependencies, zero royalties, 100% CC0.
    """

    SAMPLE_RATE = 44100

    @classmethod
    def _write_wav(cls, file_path: Path, samples: list[float]):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(file_path), "wb") as wav:
            wav.setnchannels(1)  # Mono
            wav.setsampwidth(2)   # 16-bit
            wav.setframerate(cls.SAMPLE_RATE)
            for s in samples:
                # Clamp -1.0 to 1.0
                clamped = max(-1.0, min(1.0, s))
                int_sample = int(clamped * 32767.0)
                wav.writeframesraw(struct.pack("<h", int_sample))

    @classmethod
    def generate_sub_impact(cls, output_path: Path, duration: float = 1.2) -> str:
        """Deep cinematic sub-bass impact (60Hz -> 30Hz exponential drop with natural decay)."""
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            # Frequency pitch bends down from 80Hz to 28Hz
            freq = 28.0 + 52.0 * math.exp(-t * 4.5)
            # Amplitude exponential decay
            amp = math.exp(-t * 2.8)
            # Sine wave with subtle 2nd harmonic
            s = amp * (0.85 * math.sin(2.0 * math.pi * freq * t) + 0.15 * math.sin(4.0 * math.pi * freq * t))
            samples.append(s)
        cls._write_wav(output_path, samples)
        return str(output_path.resolve())

    @classmethod
    def generate_whoosh(cls, output_path: Path, duration: float = 0.6) -> str:
        """High-velocity cinematic transition whoosh (filtered white noise & frequency sweep)."""
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        # Pseudo-random noise with modulated bandpass
        import random
        random.seed(42)
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            norm_t = t / duration
            # Bell curve volume envelope
            amp = math.sin(norm_t * math.pi) ** 2
            # Frequency pitch sweep up and down
            freq = 300.0 + 1200.0 * math.sin(norm_t * math.pi)
            noise = (random.random() * 2.0 - 1.0) * 0.4
            carrier = math.sin(2.0 * math.pi * freq * t) * 0.6
            s = amp * (carrier + noise)
            samples.append(s)
        cls._write_wav(output_path, samples)
        return str(output_path.resolve())

    @classmethod
    def generate_tactile_click(cls, output_path: Path, duration: float = 0.08) -> str:
        """High-frequency tactile glass/UI click for mockups and feature tags."""
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            amp = math.exp(-t * 80.0)
            freq = 2400.0 * math.exp(-t * 30.0)
            s = amp * math.sin(2.0 * math.pi * freq * t)
            samples.append(s)
        cls._write_wav(output_path, samples)
        return str(output_path.resolve())

    @classmethod
    def generate_shimmer(cls, output_path: Path, duration: float = 1.5) -> str:
        """Ambient metallic shimmer / bell swell for end logo reveal."""
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        partials = [520.0, 780.0, 1040.0, 1560.0, 2080.0]
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            amp = math.exp(-t * 1.8)
            s = 0.0
            for p_idx, p_freq in enumerate(partials):
                s += (0.4 / (p_idx + 1)) * math.sin(2.0 * math.pi * p_freq * t)
            samples.append(amp * s)
        cls._write_wav(output_path, samples)
        return str(output_path.resolve())

    @classmethod
    def generate_sound_library(cls, base_dir: Path) -> Dict[str, str]:
        """Generates the full sound effects suite in one call."""
        audio_dir = base_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        return {
            "sub_impact": cls.generate_sub_impact(audio_dir / "sfx_sub_impact.wav"),
            "whoosh": cls.generate_whoosh(audio_dir / "sfx_whoosh.wav"),
            "click": cls.generate_tactile_click(audio_dir / "sfx_click.wav"),
            "shimmer": cls.generate_shimmer(audio_dir / "sfx_shimmer.wav"),
        }
