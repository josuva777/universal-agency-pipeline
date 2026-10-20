import os
import sys
import platform
import ctypes
import shutil
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

# Ensure UTF-8 output on Windows safely
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

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

def get_ram_info() -> tuple[float, float, str]:
    """Returns (total_ram_gb, avail_ram_gb, confidence) across platforms."""
    if sys.platform == "win32":
        try:
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                total_gb = stat.ullTotalPhys / (1024 ** 3)
                avail_gb = stat.ullAvailPhys / (1024 ** 3)
                return (round(total_gb, 1), round(avail_gb, 1), "high (Win32 API)")
        except Exception:
            pass
    elif sys.platform == "darwin" or sys.platform.startswith("linux"):
        try:
            # Check /proc/meminfo on Linux
            if os.path.exists("/proc/meminfo"):
                with open("/proc/meminfo") as f:
                    mem = {}
                    for line in f:
                        parts = line.split(":")
                        if len(parts) == 2:
                            mem[parts[0].strip()] = int(parts[1].split()[0])
                    total_gb = mem.get("MemTotal", 8 * 1024 * 1024) / (1024 * 1024)
                    avail_gb = mem.get("MemAvailable", mem.get("MemFree", 4 * 1024 * 1024)) / (1024 * 1024)
                    return (round(total_gb, 1), round(avail_gb, 1), "high (/proc/meminfo)")
        except Exception:
            pass

    return (8.0, 4.0, "estimated (heuristic fallback)")

def get_disk_info(path: str = ".") -> tuple[float, float]:
    """Returns (free_disk_gb, total_disk_gb)."""
    try:
        total, used, free = shutil.disk_usage(path)
        return (round(free / (1024 ** 3), 1), round(total / (1024 ** 3), 1))
    except Exception:
        return (20.0, 100.0)

def get_physical_cores() -> tuple[int, int, str]:
    """Returns (physical_cores, logical_cores, confidence)."""
    logical = os.cpu_count() or 4
    if sys.platform == "win32":
        try:
            import subprocess
            out = subprocess.check_output(
                ["powershell", "-Command", "(Get-CimInstance Win32_Processor).NumberOfCores"],
                text=True, stderr=subprocess.DEVNULL
            ).strip()
            if out and out.isdigit():
                return (int(out), logical, "high (WMI)")
        except Exception:
            pass
    return (max(1, logical // 2), logical, "estimated (heuristic logical/2)")

class HardwareProfile(BaseModel):
    os_name: str
    cpu_name: str
    physical_cores: int
    logical_cores: int
    total_ram_gb: float
    available_ram_gb: float
    free_disk_gb: float
    total_disk_gb: float
    has_nvidia_gpu: bool
    gpu_name: str
    hardware_tier: Literal["tier1_light", "tier2_mid", "tier3_heavy"]
    detection_confidence: str
    recommended_local_model: str
    recommended_cloud_provider: str
    recommended_tts_engine: str
    recommended_whisper_size: str
    workload_warning: Optional[str] = None

class SystemScanner:
    """Scans host system hardware (CPU, RAM, GPU, Disk) with confidence scores,
    differentiating between Local vs Cloud compute execution profiles.
    """

    @classmethod
    def scan(cls, target_path: str = ".") -> HardwareProfile:
        total_ram, available_ram, ram_conf = get_ram_info()
        physical_cores, logical_cores, cpu_conf = get_physical_cores()
        free_disk, total_disk = get_disk_info(target_path)
        cpu_name = platform.processor() or "AMD/Intel CPU"

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

        # Workload Warning
        warning = None
        if available_ram < 3.5:
            warning = f"Low available RAM ({available_ram} GB). Heavy local models will cause memory swapping. Cloud API recommended."
        elif free_disk < 8.0:
            warning = f"Low disk space ({free_disk} GB free). Remotion 4K video rendering requires at least 8 GB free storage."

        # Tier Classification
        if total_ram <= 12.0 and not has_nvidia:
            tier = "tier1_light"
            rec_local = "qwen2.5:1.5b (Local) or Cloud API (Recommended)"
            rec_cloud = "Groq (500 tok/s free) or OpenAI gpt-4o-mini"
            rec_tts = "EdgeTTS (Zero RAM footprint)"
            rec_whisper = "tiny or base"
        elif total_ram <= 24.0 or (has_nvidia and total_ram <= 16.0):
            tier = "tier2_mid"
            rec_local = "qwen2.5:7b-instruct-q4_k_m or llama3.1:8b"
            rec_cloud = "Hybrid (Local inference with Cloud fallback)"
            rec_tts = "Kokoro ONNX local"
            rec_whisper = "small"
        else:
            tier = "tier3_heavy"
            rec_local = "qwen2.5:14b or llama3.1:70b-groq"
            rec_cloud = "Full local execution with Cloud fallback"
            rec_tts = "Kokoro ONNX / EdgeTTS"
            rec_whisper = "medium or large-v3"

        return HardwareProfile(
            os_name=f"{platform.system()} {platform.release()}",
            cpu_name=cpu_name,
            physical_cores=physical_cores,
            logical_cores=logical_cores,
            total_ram_gb=total_ram,
            available_ram_gb=available_ram,
            free_disk_gb=free_disk,
            total_disk_gb=total_disk,
            has_nvidia_gpu=has_nvidia,
            gpu_name=gpu_name,
            hardware_tier=tier,
            detection_confidence=f"RAM: {ram_conf}, CPU: {cpu_conf}",
            recommended_local_model=rec_local,
            recommended_cloud_provider=rec_cloud,
            recommended_tts_engine=rec_tts,
            recommended_whisper_size=rec_whisper,
            workload_warning=warning
        )

    @classmethod
    def display_report(cls, target_path: str = ".") -> HardwareProfile:
        profile = cls.scan(target_path)
        tier_color = "yellow" if profile.hardware_tier == "tier1_light" else "cyan" if profile.hardware_tier == "tier2_mid" else "green"

        warning_panel = f"\n[bold red]⚠️ Notice:[/bold red] {profile.workload_warning}\n" if profile.workload_warning else ""

        console.print(Panel.fit(
            f"[bold cyan]🔍 System Hardware & Model Capacity Audit[/bold cyan]\n\n"
            f"• [bold]OS:[/bold] {profile.os_name}\n"
            f"• [bold]CPU:[/bold] {profile.cpu_name} ({profile.physical_cores} Cores / {profile.logical_cores} Threads)\n"
            f"• [bold]RAM:[/bold] {profile.total_ram_gb} GB Total ({profile.available_ram_gb} GB Available at scan time)\n"
            f"• [bold]Disk Storage:[/bold] {profile.free_disk_gb} GB Free / {profile.total_disk_gb} GB Total\n"
            f"• [bold]GPU:[/bold] {profile.gpu_name} (NVIDIA CUDA: {profile.has_nvidia_gpu})\n"
            f"• [bold]Confidence:[/bold] {profile.detection_confidence}\n"
            f"• [bold]Profile Tier:[/bold] [bold {tier_color}]{profile.hardware_tier.upper()}[/bold {tier_color}]{warning_panel}\n"
            f"[bold green]Workload Execution Recommendations:[/bold green]\n"
            f"  - Local Models: [cyan]{profile.recommended_local_model}[/cyan]\n"
            f"  - Cloud APIs: [cyan]{profile.recommended_cloud_provider}[/cyan]\n"
            f"  - Neural Voice: [cyan]{profile.recommended_tts_engine}[/cyan]\n"
            f"  - Subtitles Engine: [cyan]{profile.recommended_whisper_size}[/cyan]",
            border_style="cyan"
        ))
        return profile

if __name__ == "__main__":
    SystemScanner.display_report()
