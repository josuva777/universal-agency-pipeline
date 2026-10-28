import pytest
from pathlib import Path
import tempfile
import importlib.util

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "skills" / "creative-studio" / "scripts" / "render_device_mockups.py"
spec = importlib.util.spec_from_file_location("render_device_mockups", SCRIPT_PATH)
mockup_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mockup_mod)

generate_iphone_svg = mockup_mod.generate_iphone_svg
generate_macbook_svg = mockup_mod.generate_macbook_svg
generate_interactive_3d_html = mockup_mod.generate_interactive_3d_html

def test_generate_iphone_svg():
    svg = generate_iphone_svg(style="cyber")
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "iphoneScreenClip" in svg
    assert "#10b981" in svg

def test_generate_macbook_svg():
    svg = generate_macbook_svg(style="titanium")
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "macScreenClip" in svg

def test_generate_interactive_3d_html():
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = Path(tmp_dir) / "test_viewer.html"
        generate_interactive_3d_html(style="clay", out_path=out_file)
        assert out_file.exists()
        content = out_file.read_text(encoding="utf-8")
        assert "three.min.js" in content
        assert "OrbitControls.js" in content
        assert "Clay Matte" in content

VIDEO_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "skills" / "creative-studio" / "scripts" / "generate_ai_video.py"
video_spec = importlib.util.spec_from_file_location("generate_ai_video", VIDEO_SCRIPT_PATH)
video_mod = importlib.util.module_from_spec(video_spec)
video_spec.loader.exec_module(video_mod)
AIVideoDirector = video_mod.AIVideoDirector

def test_ai_video_director_storyboard():
    director = AIVideoDirector(project_name="NovaGuard AI", out_dir=Path("."))
    storyboard = director.generate_storyboard("Next-gen AI security platform")
    assert len(storyboard) == 5
    assert storyboard[0]["name"] == "Dopamine Hook"
    assert "NovaGuard AI" in storyboard[2]["voiceover"]

def test_ai_video_director_subtitles_and_remotion():
    with tempfile.TemporaryDirectory() as tmp_dir:
        director = AIVideoDirector(project_name="NovaGuard AI", out_dir=Path(tmp_dir))
        manifest = director.generate_all("Automated agent fleet")
        assert manifest["duration_seconds"] == 30.0
        assert manifest["fps"] == 60
        assert (Path(tmp_dir) / "storyboard.json").exists()
        assert (Path(tmp_dir) / "whisper_subtitles.json").exists()
        assert (Path(tmp_dir) / "CommercialComposition.tsx").exists()
        tsx = (Path(tmp_dir) / "CommercialComposition.tsx").read_text(encoding="utf-8")
        assert "Commercial16x9" in tsx
        assert "Commercial9x16" in tsx
        assert "SubtitlesOverlay" in tsx

