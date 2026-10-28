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
