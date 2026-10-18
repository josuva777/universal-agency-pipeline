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
    """Generates customized commercial script & scenes with automatic multi-model failover (Gemini -> Groq -> OpenAI -> Offline Engine)."""
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

    # 1. Primary: Google Gemini (Free Tier)
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key and gemini_key != "your_gemini_api_key_here":
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_text)
                    console.print("[dim green]✓ Script generated via Google Gemini[/dim green]")
                    return CommercialScript(**parsed)
                else:
                    console.print(f"[dim yellow]Gemini returned status {res.status_code}, falling back...[/dim yellow]")
        except Exception as e:
            console.print(f"[dim yellow]Notice: Gemini bypassed: {e}, attempting fallback...[/dim yellow]")

    # 2. Secondary: Groq Llama 3.3 70B (100% Free Tier, 500 tokens/sec)
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here":
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are an elite creative director. Respond with pure JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"}
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    raw_text = res.json()["choices"][0]["message"]["content"]
                    parsed = json.loads(raw_text)
                    console.print("[dim green]✓ Script generated via Groq (Llama 3.3 70B)[/dim green]")
                    return CommercialScript(**parsed)
        except Exception as e:
            console.print(f"[dim yellow]Notice: Groq bypassed: {e}, attempting next fallback...[/dim yellow]")

    # 3. Tertiary: OpenAI (gpt-4o-mini)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_api_key_here":
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {openai_key}"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are an elite creative director. Respond with pure JSON only."},
                    {"role": "user", "content": prompt}
                ],
                "response_format": {"type": "json_object"}
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    raw_text = res.json()["choices"][0]["message"]["content"]
                    parsed = json.loads(raw_text)
                    console.print("[dim green]✓ Script generated via OpenAI (GPT-4o-mini)[/dim green]")
                    return CommercialScript(**parsed)
        except Exception as e:
            console.print(f"[dim yellow]Notice: OpenAI bypassed: {e}[/dim yellow]")

    # 4. Final: Deterministic Built-in Offline Engine (100% Guaranteed Success, Zero Network Required)
    console.print("[dim cyan]✓ Using Deterministic Master Baseline Script[/dim cyan]")
    return CommercialScript(
        project_title=f"{brand_slug} Commercial",
        brand_name=brand_slug,
        tagline=chosen_style["tagline"],
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
        "logoSvgPath": str(Path(logo_meta["svg_path"]).resolve())
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

    console.print(Panel.fit(
        f"[bold green]✨ Creative Studio Production Package Ready![/bold green]\n"
        f"• Interactive Client Portal: [link={portal_path}]{portal_path}[/link]\n"
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
    output: str = typer.Option("./assets/outputs/production_run", "--output", "-o", help="Output directory"),
    style: str = typer.Option("fintech", "--style", "-s", help="Aesthetic preset: fintech | saas | streetwear | editorial")
):
    """Executes end-to-end multi-agent creative commercial production."""
    asyncio.run(run_creative_pipeline(brief, output, style=style))

if __name__ == "__main__":
    app()
