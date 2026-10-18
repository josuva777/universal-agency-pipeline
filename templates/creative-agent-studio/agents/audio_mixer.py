import os
import shutil
import asyncio
import subprocess
from pathlib import Path
from typing import List, Optional

class AudioMixer:
    """Master Audio Mixing & Mastering Engine using FFmpeg with EBU R128 broadcast standards and sidechain ducking."""

    @classmethod
    def find_ffmpeg(cls) -> Optional[str]:
        # 1. System PATH
        cmd = shutil.which("ffmpeg")
        if cmd:
            return cmd
        
        # 2. Local standard locations
        possible_paths = [
            Path("C:/ffmpeg/bin/ffmpeg.exe"),
            Path("C:/Program Files/ffmpeg/bin/ffmpeg.exe"),
            Path("C:/Users/ELCOT/AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe"),
            Path("C:/Users/ELCOT/.local/bin/ffmpeg.exe"),
        ]
        for p in possible_paths:
            if p.exists():
                return str(p)
        return None

    @classmethod
    async def mix_voiceover_with_music(
        cls,
        voice_path: str,
        music_path: str,
        output_path: str,
        ducking_attenuation_db: float = 12.0,
        target_lufs: float = -14.0,
    ) -> str:
        """Ducks background music under spoken voiceover and applies EBU R128 mastering."""
        ffmpeg_bin = cls.find_ffmpeg() or "ffmpeg"
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        # Filter explanation:
        # 1. [0:a] is music, [1:a] is voiceover
        # 2. sidechaincompress ducks music when voiceover is present
        # 3. amix blends ducked music and clear voiceover
        # 4. loudnorm normalizes to -14 LUFS with True Peak at -1.0 dBFS
        filter_str = (
            f"[0:a][1:a]sidechaincompress=threshold=0.08:ratio=6:attack=20:release=300[ducked_music];"
            f"[ducked_music][1:a]amix=inputs=2:duration=first:dropout_transition=2[mixed];"
            f"[mixed]loudnorm=I={target_lufs}:LRA=7:TP=-1.0[out]"
        )

        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", str(Path(music_path).resolve()),
            "-i", str(Path(voice_path).resolve()),
            "-filter_complex", filter_str,
            "-map", "[out]",
            "-c:a", "pcm_s16le",
            "-ar", "48000",
            str(out.resolve()),
        ]

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                # If sidechain filter fails (e.g. missing files), fall back to simple copy of voice
                shutil.copyfile(voice_path, output_path)
        except Exception:
            # Fallback if FFmpeg execution fails
            shutil.copyfile(voice_path, output_path)

        return str(out.resolve())

    @classmethod
    async def overlay_sfx(
        cls,
        base_audio_path: str,
        sfx_path: str,
        timestamp_seconds: float,
        output_path: str
    ) -> str:
        """Overlays a transient sound effect (riser, whoosh, click) at an exact millisecond marker."""
        ffmpeg_bin = cls.find_ffmpeg() or "ffmpeg"
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        delay_ms = int(timestamp_seconds * 1000)

        filter_str = (
            f"[1:a]adelay={delay_ms}|{delay_ms}[delayed_sfx];"
            f"[0:a][delayed_sfx]amix=inputs=2:duration=first[out]"
        )

        cmd = [
            ffmpeg_bin,
            "-y",
            "-i", str(Path(base_audio_path).resolve()),
            "-i", str(Path(sfx_path).resolve()),
            "-filter_complex", filter_str,
            "-map", "[out]",
            str(out.resolve())
        ]

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
        except Exception:
            shutil.copyfile(base_audio_path, output_path)

        return str(out.resolve())
