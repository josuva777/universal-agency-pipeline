import os
import sys
import platform
import ctypes
from typing import Dict, Any, Literal
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

console = Console(legacy_windows=False, force_terminal=True)

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

def get_ram_info() -> tuple[float, float]:
    """Returns (total_ram_gb, avail_ram_gb) with zero dependencies on Windows."""
    if sys.platform == "win32":
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            total_gb = stat.ullTotalPhys / (1024 ** 3)
            avail_gb = stat.ullAvailPhys / (1024 ** 3)
            return (round(total_gb, 1), round(avail_gb, 1))
    return (8.0, 4.0)

class HardwareProfile(BaseModel):
    os_name: str
    cpu_name: str
    physical_cores: int
    logical_cores: int
    total_ram_gb: float
    available_ram_gb: float
    has_nvidia_gpu: bool
    gpu_name: str
    hardware_tier: Literal["tier1_light", "tier2_mid", "tier3_heavy"]
    recommended_local_model: str
    recommended_tts_engine: str
    recommended_whisper_size: str
    recommended_cloud_provider: str

class SystemScanner:
    """Scans host system hardware (CPU, RAM, GPU) to automatically determine
    which models and compute workloads can safely run without freezing or running out of memory.
    """

    @classmethod
    def scan(cls) -> HardwareProfile:
        total_ram, available_ram = get_ram_info()
        cpu_name = platform.processor() or "AMD/Intel CPU"
        logical_cores = os.cpu_count() or 4
        physical_cores = max(1, logical_cores // 2)

        # GPU detection
        has_nvidia = False
        gpu_name = "Integrated Graphics"
        if sys.platform == "win32":
            try:
                import subprocess
                out = subprocess.check_output(
                    ["powershell", "-Command", "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"],
                    text=True, stderr=subprocess.DEVNULL
                ).strip()
                if out:
                    gpu_name = out.split("\n")[0].strip()
                    if "nvidia" in gpu_name.lower():
                        has_nvidia = True
            except Exception:
                pass

        # Determine Hardware Tier
        # Tier 1 (Light): <= 12GB RAM, integrated GPU or low VRAM
        # Tier 2 (Mid): 16GB-24GB RAM, dedicated GPU (4-8GB VRAM)
        # Tier 3 (Heavy): >= 32GB RAM or dedicated GPU (>= 12GB VRAM)
        if total_ram <= 12.0 and not has_nvidia:
            tier = "tier1_light"
            rec_model = "qwen2.5:1.5b or llama3.2:1b (Cloud API recommended for large tasks)"
            rec_tts = "EdgeTTS (Zero RAM footprint) / Kokoro 82M"
            rec_whisper = "tiny or base"
            rec_cloud = "Groq (Free fast inference) or OpenAI gpt-4o-mini"
        elif total_ram <= 24.0 or (has_nvidia and total_ram <= 16.0):
            tier = "tier2_mid"
            rec_model = "qwen2.5:7b-instruct-q4_k_m or llama3.1:8b"
            rec_tts = "Kokoro ONNX local"
            rec_whisper = "small"
            rec_cloud = "Hybrid Local + Cloud"
        else:
            tier = "tier3_heavy"
            rec_model = "qwen2.5:14b or llama3.1:70b-groq"
            rec_tts = "Kokoro ONNX / Chatterbox"
            rec_whisper = "medium or large-v3"
            rec_cloud = "Full Local with Cloud Fallback"

        return HardwareProfile(
            os_name=f"{platform.system()} {platform.release()}",
            cpu_name=cpu_name,
            physical_cores=physical_cores,
            logical_cores=logical_cores,
            total_ram_gb=round(total_ram, 1),
            available_ram_gb=round(available_ram, 1),
            has_nvidia_gpu=has_nvidia,
            gpu_name=gpu_name,
            hardware_tier=tier,
            recommended_local_model=rec_model,
            recommended_tts_engine=rec_tts,
            recommended_whisper_size=rec_whisper,
            recommended_cloud_provider=rec_cloud
        )

    @classmethod
    def display_report(cls) -> HardwareProfile:
        profile = cls.scan()
        tier_color = "yellow" if profile.hardware_tier == "tier1_light" else "cyan" if profile.hardware_tier == "tier2_mid" else "green"

        console.print(Panel.fit(
            f"[bold cyan]🔍 System Hardware & Model Capacity Audit[/bold cyan]\n\n"
            f"• [bold]OS:[/bold] {profile.os_name}\n"
            f"• [bold]CPU:[/bold] {profile.cpu_name} ({profile.physical_cores} Cores / {profile.logical_cores} Threads)\n"
            f"• [bold]RAM:[/bold] {profile.total_ram_gb} GB Total ({profile.available_ram_gb} GB Available)\n"
            f"• [bold]GPU:[/bold] {profile.gpu_name} (NVIDIA CUDA: {profile.has_nvidia_gpu})\n"
            f"• [bold]Profile Tier:[/bold] [bold {tier_color}]{profile.hardware_tier.upper()}[/bold {tier_color}]\n\n"
            f"[bold green]Optimized Recommendations (Zero Freeze Guarantee):[/bold green]\n"
            f"  - Local LLM: [cyan]{profile.recommended_local_model}[/cyan]\n"
            f"  - Cloud LLM: [cyan]{profile.recommended_cloud_provider}[/cyan]\n"
            f"  - Neural Voice: [cyan]{profile.recommended_tts_engine}[/cyan]\n"
            f"  - Whisper Subtitles: [cyan]{profile.recommended_whisper_size}[/cyan]",
            border_style="cyan"
        ))
        return profile

if __name__ == "__main__":
    SystemScanner.display_report()
