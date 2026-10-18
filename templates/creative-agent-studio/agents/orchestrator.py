import os
import sys
import json
import asyncio
from pathlib import Path
from typing import TypedDict, List, Dict, Any, Optional
import typer
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

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

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

async def run_creative_pipeline(brief: str, output_directory: str) -> Dict[str, Any]:
    out_dir = Path(output_directory)
    out_dir.mkdir(parents=True, exist_ok=True)
    video_dir = out_dir / "video_assets"
    video_dir.mkdir(parents=True, exist_ok=True)

    console.print(Panel.fit(
        f"[bold cyan]🎬 Creative Studio AI Orchestrator[/bold cyan]\n"
        f"[dim]Brief:[/dim] {brief}\n"
        f"[dim]Output:[/dim] {out_dir.resolve()}",
        border_style="cyan"
    ))

    # 1. Script & Visual Scene Planning
    console.print("[bold yellow]⚡ Phase 1: Directing Script & 3D Scene Architecture...[/bold yellow]")
    # Deterministic high-converting agency commercial script
    brand_slug = "".join([c for c in brief.split()[0] if c.isalnum()]).capitalize() or "Apex"
    script = CommercialScript(
        project_title=f"{brand_slug} Commercial",
        brand_name=brand_slug,
        tagline="INTELLIGENCE AMPLIFIED",
        voiceover_script=(
            f"The future isn't coming. It's already here. "
            f"Meet {brand_slug}. Engineered from the ground up for breakthrough performance, "
            f"uncompromising precision, and absolute speed. "
            f"Step into the next era today."
        ),
        scenes=[
            ScenePlan(id=1, type="hero", headline="THE NEXT ERA", subtext="Speed Without Compromise", duration_seconds=3.0, vfx_type="particles"),
            ScenePlan(id=2, type="tension", headline="RETHINK EVERYTHING", subtext="Legacy tools hold you back", duration_seconds=3.5, vfx_type="chromatic"),
            ScenePlan(id=3, type="mockup_3d", headline="ENGINEERED PRECISION", subtext="3D Architecture at scale", duration_seconds=5.0, vfx_type="glow"),
            ScenePlan(id=4, type="metrics", headline="+400% FASTER", subtext="Validated by industry benchmarks", duration_seconds=3.5, vfx_type="particles"),
            ScenePlan(id=5, type="cta", headline=brand_slug.upper(), subtext="Start Free Today", duration_seconds=4.0, vfx_type="glow"),
        ],
        primary_color="#6366f1",
        secondary_color="#8b5cf6",
        accent_color="#06b6d4"
    )

    # 2. Neural Audio Voiceover Synthesis
    console.print("[bold green]🎙️ Phase 2: Synthesizing Microsoft Neural Voiceover...[/bold green]")
    audio_path = str(out_dir / "voiceover.wav")
    voice_res = await VoiceEngine.synthesize(
        text=script.voiceover_script,
        output_path=audio_path,
        voice="en-US-GuyNeural"
    )
    console.print(f"  ✓ Voiceover generated: {voice_res.duration_seconds:.2f}s with {len(voice_res.word_timestamps)} word boundaries")

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
        "logoSvgPath": str(Path(logo_meta["svg_path"]).resolve())
    }

    props_file = out_dir / "remotion_props.json"
    with open(props_file, "w", encoding="utf-8") as f:
        json.dump(remotion_props, f, indent=2)

    console.print(f"  ✓ Remotion configuration payload written to: {props_file}")

    console.print(Panel.fit(
        f"[bold green]✨ Creative Studio Production Package Ready![/bold green]\n"
        f"• Voiceover: {audio_path}\n"
        f"• Subtitles: {srt_path}\n"
        f"• Logo Suite: {logo_meta['svg_path']}\n"
        f"• Remotion Payload: {props_file}\n\n"
        f"[bold cyan]To render 4K video:[/bold cyan]\n"
        f"cd video && npx remotion render src/index.ts Commercial --props={props_file} --output={out_dir}/commercial_master.mp4",
        border_style="green"
    ))

    return remotion_props

app = typer.Typer(help="Creative Studio CLI Orchestrator")

@app.command()
def produce(
    brief: str = typer.Option(..., "--brief", "-b", help="Client creative brief description"),
    output: str = typer.Option("./assets/outputs/production_run", "--output", "-o", help="Output directory")
):
    """Executes end-to-end multi-agent creative commercial production."""
    asyncio.run(run_creative_pipeline(brief, output))

if __name__ == "__main__":
    app()
