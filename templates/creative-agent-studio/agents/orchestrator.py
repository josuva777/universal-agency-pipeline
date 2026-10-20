import os
import sys
import json
import asyncio
from pathlib import Path
from typing import TypedDict, List, Dict, Any, Optional
import httpx
import typer
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pydantic import BaseModel, Field

# Local Agents
from agents.voice_engine import VoiceEngine, VoiceoverResult
from agents.transcriber import AudioTranscriber, CaptionSegment
from agents.audio_mixer import AudioMixer
from agents.broll_fetcher import BRollFetcher, BRollClip
from agents.logo_generator import LogoGenerator, BrandPalette
from agents.sfx_generator import ProceduralSFXGenerator
from agents.brand_kit_exporter import BrandKitExporter
from agents.model_provider import CentralizedModelProvider

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

class ScenePlan(BaseModel):
    id: int
    type: str  # "hero" | "tension" | "mockup_3d" | "metrics" | "cta"
    headline: str
    subtext: str
    duration_seconds: float
    vfx_type: str = "particles"  # "particles" | "chromatic" | "glow"

class CommercialScript(BaseModel):
    project_title: str
    brand_name: str
    tagline: str
    voiceover_script: str
    scenes: List[ScenePlan]
    primary_color: str = "#6366f1"
    secondary_color: str = "#8b5cf6"
    accent_color: str = "#d946ef"

class CreativeProductionState(TypedDict):
    brief: str
    output_dir: str
    script: Optional[CommercialScript]
    voice_result: Optional[VoiceoverResult]
    captions: List[CaptionSegment]
    logo_svg_path: Optional[str]
    broll_clips: List[BRollClip]
    remotion_props_path: Optional[str]
    status: str

STYLE_PRESETS = {
    "fintech": {
        "primary": "#6366f1",
        "secondary": "#8b5cf6",
        "accent": "#06b6d4",
        "voice": "en-US-GuyNeural",
        "tagline": "INTELLIGENCE REDEFINED",
    },
    "saas": {
        "primary": "#3b82f6",
        "secondary": "#6366f1",
        "accent": "#10b981",
        "voice": "en-US-AriaNeural",
        "tagline": "WORKFLOW ACCELERATED",
    },
    "streetwear": {
        "primary": "#f43f5e",
        "secondary": "#fb923c",
        "accent": "#facc15",
        "voice": "en-US-ChristopherNeural",
        "tagline": "UNSTOPPABLE MOMENTUM",
    },
    "editorial": {
        "primary": "#eab308",
        "secondary": "#f472b6",
        "accent": "#2dd4bf",
        "voice": "en-GB-SoniaNeural",
        "tagline": "EXCELLENCE IN EVERY DETAIL",
    },
}

async def generate_script_with_ai(brief: str, chosen_style: dict) -> CommercialScript:
    """Generates customized commercial script & scenes with automatic multi-model failover."""
    brand_slug = "".join([c for c in brief.split()[0] if c.isalnum()]).capitalize() or "Apex"

    prompt = (
        f"You are an elite creative commercial director. Create a 20-second commercial script and scene plan for:\n"
        f"Brief: {brief}\n\n"
        f"Respond with ONLY a valid JSON object matching this structure:\n"
        f"{{\n"
        f'  "project_title": "{brand_slug} Commercial",\n'
        f'  "brand_name": "{brand_slug}",\n'
        f'  "tagline": "SHORT PUNCHY TAGLINE",\n'
        f'  "voiceover_script": "Engaging punchy 3-sentence voiceover script for audio narration",\n'
        f'  "primary_color": "{chosen_style["primary"]}",\n'
        f'  "secondary_color": "{chosen_style["secondary"]}",\n'
        f'  "accent_color": "{chosen_style["accent"]}",\n'
        f'  "scenes": [\n'
        f'    {{"id": 1, "type": "hero", "headline": "HEADLINE", "subtext": "Subtext", "duration_seconds": 3.0, "vfx_type": "particles"}},\n'
        f'    {{"id": 2, "type": "tension", "headline": "HEADLINE", "subtext": "Subtext", "duration_seconds": 3.5, "vfx_type": "chromatic"}},\n'
        f'    {{"id": 3, "type": "mockup_3d", "headline": "HEADLINE", "subtext": "Subtext", "duration_seconds": 5.0, "vfx_type": "glow"}},\n'
        f'    {{"id": 4, "type": "metrics", "headline": "HEADLINE", "subtext": "Subtext", "duration_seconds": 3.5, "vfx_type": "particles"}},\n'
        f'    {{"id": 5, "type": "cta", "headline": "{brand_slug.upper()}", "subtext": "Subtext", "duration_seconds": 4.0, "vfx_type": "glow"}}\n'
        f'  ]\n'
        f"}}"
    )

    # Multi-model provider execution with centralized 2026 failover
    provider = CentralizedModelProvider()
    parsed_json, source = await provider.generate_json(prompt)

    if parsed_json:
        try:
            console.print(f"[dim green]✓ Commercial script generated via {source}[/dim green]")
            return CommercialScript(**parsed_json)
        except Exception as e:
            console.print(f"[dim yellow]Notice: Script schema validation failed ({e}), using baseline...[/dim yellow]")

    # Deterministic Truth-in-Marketing Master Baseline Script
    console.print("[dim cyan]✓ Using Deterministic Master Baseline Script (Truth-in-Marketing Certified)[/dim cyan]")
    return CommercialScript(
        project_title=f"{brand_slug} Commercial",
        brand_name=brand_slug,
        tagline=chosen_style["tagline"],
        voiceover_script=(
            f"The future isn't coming. It's already here. "
            f"Meet {brand_slug}. Engineered from the ground up for breakthrough performance, "
            f"uncompromising precision, and streamlined execution. "
            f"Step into the next era today."
        ),
        scenes=[
            ScenePlan(id=1, type="hero", headline="THE NEXT ERA", subtext="Precision Engineered", duration_seconds=3.0, vfx_type="particles"),
            ScenePlan(id=2, type="tension", headline="RETHINK EVERYTHING", subtext="Legacy workflows hold you back", duration_seconds=3.5, vfx_type="chromatic"),
            ScenePlan(id=3, type="mockup_3d", headline="ENGINEERED PRECISION", subtext="3D Architecture at scale", duration_seconds=5.0, vfx_type="glow"),
            ScenePlan(id=4, type="metrics", headline="PROVEN IMPACT", subtext="Measurable Performance at Scale", duration_seconds=3.5, vfx_type="particles"),
            ScenePlan(id=5, type="cta", headline=brand_slug.upper(), subtext="Deploy with Confidence", duration_seconds=4.0, vfx_type="glow"),
        ],
        primary_color=chosen_style["primary"],
        secondary_color=chosen_style["secondary"],
        accent_color=chosen_style["accent"]
    )

async def run_creative_pipeline(brief: str, output_directory: str, style: str = "fintech") -> Dict[str, Any]:
    out_dir = Path(output_directory)
    out_dir.mkdir(parents=True, exist_ok=True)
    video_dir = out_dir / "video_assets"
    video_dir.mkdir(parents=True, exist_ok=True)

    chosen_style = STYLE_PRESETS.get(style.lower(), STYLE_PRESETS["fintech"])

    console.print(Panel.fit(
        f"[bold cyan]🎬 Creative Studio AI Orchestrator[/bold cyan]\n"
        f"[dim]Brief:[/dim] {brief}\n"
        f"[dim]Aesthetic Style Preset:[/dim] [bold yellow]{style.upper()}[/bold yellow]\n"
        f"[dim]Output Directory:[/dim] {out_dir.resolve()}",
        border_style="cyan"
    ))

    # 1. Script & Visual Scene Planning
    console.print("[bold yellow]⚡ Phase 1: Directing Script & 3D Scene Architecture...[/bold yellow]")
    script = await generate_script_with_ai(brief, chosen_style)
    console.print(f"  ✓ Script ready for [bold cyan]{script.brand_name}[/bold cyan] ('{script.tagline}')")

    # 2. Neural Audio Voiceover Synthesis + Procedural SFX Library
    console.print("[bold green]🎙️ Phase 2: Synthesizing Neural Voiceover & Sound Effects...[/bold green]")
    audio_path = str(out_dir / "voiceover.wav")
    voice_res = await VoiceEngine.synthesize(
        text=script.voiceover_script,
        output_path=audio_path,
        voice=chosen_style["voice"]
    )
    console.print(f"  ✓ Voiceover generated ({chosen_style['voice']}): {voice_res.duration_seconds:.2f}s")

    # Generate CC0 sound library into assets/audio
    assets_dir = out_dir.resolve().parents[1] if len(out_dir.resolve().parents) > 1 else out_dir.resolve().parent
    sfx_files = ProceduralSFXGenerator.generate_sound_library(assets_dir)
    console.print(f"  ✓ CC0 Micro-SFX suite ready ({len(sfx_files)} sound effects generated)")

    # 3. Subtitles & Karaoke Word Alignment
    console.print("[bold cyan]📝 Phase 3: Generating Millisecond Karaoke Captions...[/bold cyan]")
    caption_segments = [
        CaptionSegment(
            word=wt.word,
            start_seconds=wt.start_ms / 1000.0,
            end_seconds=wt.end_ms / 1000.0
        ) for wt in voice_res.word_timestamps
    ]
    srt_path = str(out_dir / "subtitles.srt")
    AudioTranscriber.generate_srt(caption_segments, srt_path)
    console.print(f"  ✓ SRT Subtitles created at: {srt_path}")

    # 4. Procedural Vector Brand Logo Generation
    console.print("[bold magenta]🎨 Phase 4: Constructing Procedural Vector Logo Suite...[/bold magenta]")
    palette = BrandPalette(
        primary=script.primary_color,
        secondary=script.secondary_color,
        accent=script.accent_color
    )
    logo_meta = LogoGenerator.save_logo_suite(
        brand_name=script.brand_name,
        output_dir=str(out_dir),
        tagline=script.tagline,
        palette=palette
    )
    console.print(f"  ✓ Vector Logo SVG created: {logo_meta['svg_path']}")

    # 5. B-Roll Footage Discovery & Archiving
    console.print("[bold blue]📹 Phase 5: Fetching 4K Commercial Footage...[/bold blue]")
    fetcher = BRollFetcher()
    broll_clips = await fetcher.search_clips(query="technology abstract 4k", count=2)
    console.print(f"  ✓ Found {len(broll_clips)} high-definition cinematic b-roll clips")

    # 6. Remotion Props Composition Contract
    console.print("[bold red]🎬 Phase 6: Assembling Remotion Production Contract...[/bold red]")
    remotion_props = {
        "projectName": script.project_title,
        "brandName": script.brand_name,
        "tagline": script.tagline,
        "fps": 60,
        "durationInFrames": int(voice_res.duration_seconds * 60) + 120,
        "theme": {
            "primary": script.primary_color,
            "secondary": script.secondary_color,
            "accent": script.accent_color,
            "background": "#0a0b0e"
        },
        "scenes": [s.model_dump() for s in script.scenes],
        "voiceoverAudioPath": str(Path(audio_path).resolve()),
        "subtitles": [c.model_dump() for c in caption_segments],
        "logoSvgPath": str(Path(logo_meta["svg_path"]).resolve()),
        "brollClips": [b.model_dump() for b in broll_clips]
    }

    props_file = out_dir / "remotion_props.json"
    with open(props_file, "w", encoding="utf-8") as f:
        json.dump(remotion_props, f, indent=2)
    console.print(f"  ✓ Remotion configuration payload written to: {props_file}")

    # 7. Executive Client Brand & Deliverables Portal
    console.print("[bold white]🌐 Phase 7: Generating Executive Client Brand Portal...[/bold white]")
    with open(logo_meta["svg_path"], "r", encoding="utf-8") as f:
        svg_raw = f.read()

    portal_path = BrandKitExporter.generate_portal(
        output_dir=out_dir,
        brand_name=script.brand_name,
        tagline=script.tagline,
        palette={"primary": script.primary_color, "secondary": script.secondary_color, "accent": script.accent_color},
        svg_content=svg_raw,
        script_text=script.voiceover_script,
        voiceover_rel_path="voiceover.wav",
        subtitles_rel_path="subtitles.srt"
    )
    console.print(f"  ✓ Interactive Client Portal created: {portal_path}")

    # 8. Optional Automated Video Rendering Subprocess
    rendered_video_path = None
    if render_video:
        console.print("[bold cyan]🎬 Phase 8: Executing Remotion Video Render Subprocess...[/bold cyan]")
        import shutil
        import subprocess

        video_project_dir = Path(__file__).resolve().parent.parent / "video"
        output_mp4 = out_dir / "commercial_master.mp4"
        npx_cmd = shutil.which("npx") or ("npx.cmd" if sys.platform == "win32" else None)

        if npx_cmd and video_project_dir.exists():
            cmd = [
                npx_cmd,
                "remotion",
                "render",
                "src/index.tsx",
                "Commercial",
                f"--props={str(props_file.resolve())}",
                f"--output={str(output_mp4.resolve())}",
            ]
            try:
                res = subprocess.run(cmd, cwd=str(video_project_dir), capture_output=True, text=True, timeout=300)
                if res.returncode == 0 and output_mp4.exists():
                    rendered_video_path = str(output_mp4)
                    console.print(f"  ✓ Rendered master video: [bold green]{output_mp4}[/bold green]")
                else:
                    console.print(f"  [yellow]Notice: Remotion exited ({res.returncode}). Command available to run manually.[/yellow]")
            except Exception as e:
                console.print(f"  [yellow]Subprocess render notice: {e}[/yellow]")
        else:
            console.print("  [dim]npx or video template not present in local path; rendering command generated.[/dim]")

    render_status_line = (
        f"• Rendered Master Video: [bold green]{rendered_video_path}[/bold green]\n"
        if rendered_video_path else
        f"[bold cyan]To render 4K video manually:[/bold cyan]\ncd video && npx remotion render src/index.tsx Commercial --props={props_file} --output={out_dir}/commercial_master.mp4\n"
    )

    console.print(Panel.fit(
        f"[bold green]✨ Creative Studio Production Package Ready![/bold green]\n"
        f"• Interactive Client Portal: [link={portal_path}]{portal_path}[/link]\n"
        f"• Voiceover: {audio_path}\n"
        f"• Subtitles: {srt_path}\n"
        f"• Logo Suite: {logo_meta['svg_path']}\n"
        f"• Remotion Payload: {props_file}\n"
        f"• B-Roll Clips Attached: {len(broll_clips)}\n\n"
        f"{render_status_line}",
        border_style="green"
    ))

    return remotion_props

app = typer.Typer(help="Creative Studio CLI Orchestrator")

@app.command()
def produce(
    brief: str = typer.Option(..., "--brief", "-b", help="Client creative brief description"),
    output: str = typer.Option("./assets/outputs/production_run", "--output", "-o", help="Output directory"),
    style: str = typer.Option("fintech", "--style", "-s", help="Aesthetic preset: fintech | saas | streetwear | editorial"),
    render: bool = typer.Option(False, "--render", "-r", help="Automatically execute Remotion render subprocess to produce .mp4")
):
    """Executes end-to-end multi-agent creative commercial production."""
    asyncio.run(run_creative_pipeline(brief, output, style=style, render_video=render))

if __name__ == "__main__":
    app()
