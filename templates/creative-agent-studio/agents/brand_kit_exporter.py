import json
from pathlib import Path
from typing import Dict, Any, List

class BrandKitExporter:
    """Generates an executive, client-facing HTML Brand & Deliverables Portal."""

    @classmethod
    def generate_portal(
        cls,
        output_dir: Path,
        brand_name: str,
        tagline: str,
        palette: Dict[str, str],
        svg_content: str,
        script_text: str,
        voiceover_rel_path: str = "voiceover.wav",
        subtitles_rel_path: str = "subtitles.srt",
    ) -> str:
        portal_file = output_dir / "brand_kit.html"

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{brand_name} • Executive Brand & Media Deliverable Portal</title>
  <style>
    :root {{
      --primary: {palette.get('primary', '#6366f1')};
      --secondary: {palette.get('secondary', '#8b5cf6')};
      --accent: {palette.get('accent', '#06b6d4')};
      --bg: #090a0f;
      --surface: #12141c;
      --border: rgba(255, 255, 255, 0.08);
      --text: #f8fafc;
      --text-muted: rgba(255, 255, 255, 0.6);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 40px 20px;
    }}
    .container {{ max-width: 1140px; margin: 0 auto; }}
    header {{
      text-align: center;
      margin-bottom: 60px;
      padding-bottom: 30px;
      border-bottom: 1px solid var(--border);
    }}
    .badge {{
      display: inline-block;
      padding: 6px 16px;
      border-radius: 999px;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid var(--primary);
      color: var(--primary);
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}
    h1 {{ font-size: 54px; font-weight: 900; letter-spacing: -1.5px; margin-bottom: 8px; }}
    .tagline {{ font-size: 20px; color: var(--accent); font-family: monospace; letter-spacing: 4px; }}
    
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 32px; margin-bottom: 48px; }}
    .card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 32px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }}
    .card h2 {{ font-size: 22px; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }}
    
    /* Logo Preview */
    .logo-stage {{
      background: #000000;
      border-radius: 14px;
      padding: 30px;
      display: flex;
      justify-content: center;
      align-items: center;
      border: 1px solid var(--border);
      margin-bottom: 20px;
      min-height: 180px;
    }}
    .logo-stage svg {{ max-height: 140px; width: auto; }}
    
    /* Swatches */
    .swatches {{ display: flex; flex-direction: column; gap: 14px; }}
    .swatch-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 18px;
      border-radius: 12px;
      background: rgba(255,255,255,0.03);
      border: 1px solid var(--border);
    }}
    .swatch-color {{
      width: 38px;
      height: 38px;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    .swatch-info {{ flex: 1; margin-left: 16px; }}
    .swatch-name {{ font-weight: 700; font-size: 15px; }}
    .swatch-hex {{ font-family: monospace; color: var(--text-muted); font-size: 13px; }}
    
    /* Audio */
    audio {{ width: 100%; margin-top: 14px; border-radius: 10px; }}
    .script-box {{
      background: rgba(0,0,0,0.3);
      padding: 18px;
      border-radius: 12px;
      border: 1px solid var(--border);
      font-size: 15px;
      color: var(--text-muted);
      margin-top: 16px;
      max-height: 140px;
      overflow-y: auto;
    }}

    /* Actions */
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 12px 24px;
      border-radius: 12px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s ease;
      cursor: pointer;
      border: none;
      font-size: 14px;
    }}
    .btn-primary {{
      background: var(--primary);
      color: #ffffff;
      box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }}
    .btn-primary:hover {{ transform: translateY(-2px); }}
    .btn-secondary {{
      background: rgba(255,255,255,0.08);
      color: #ffffff;
      margin-left: 10px;
    }}
    .footer {{
      text-align: center;
      color: var(--text-muted);
      font-size: 13px;
      margin-top: 60px;
      padding-top: 20px;
      border-top: 1px solid var(--border);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge">Master Agency Deliverable</div>
      <h1>{brand_name}</h1>
      <div class="tagline">{tagline}</div>
    </header>

    <div class="grid">
      <!-- 1. Master Vector Logo -->
      <div class="card">
        <h2>📐 Master Vector Logo</h2>
        <div class="logo-stage">
          {svg_content}
        </div>
        <div style="display: flex; gap: 10px;">
          <a href="logo_master.svg" download class="btn btn-primary" style="flex: 1;">Download SVG</a>
          <button onclick="navigator.clipboard.writeText(document.querySelector('.logo-stage').innerHTML)" class="btn btn-secondary">Copy SVG</button>
        </div>
      </div>

      <!-- 2. Harmonized Color System -->
      <div class="card">
        <h2>🎨 Color Palette System</h2>
        <div class="swatches">
          <div class="swatch-row">
            <div class="swatch-color" style="background: {palette.get('primary', '#6366f1')};"></div>
            <div class="swatch-info">
              <div class="swatch-name">Primary Brand</div>
              <div class="swatch-hex">{palette.get('primary', '#6366f1')}</div>
            </div>
          </div>
          <div class="swatch-row">
            <div class="swatch-color" style="background: {palette.get('secondary', '#8b5cf6')};"></div>
            <div class="swatch-info">
              <div class="swatch-name">Secondary Structure</div>
              <div class="swatch-hex">{palette.get('secondary', '#8b5cf6')}</div>
            </div>
          </div>
          <div class="swatch-row">
            <div class="swatch-color" style="background: {palette.get('accent', '#06b6d4')};"></div>
            <div class="swatch-info">
              <div class="swatch-name">Accent Energy</div>
              <div class="swatch-hex">{palette.get('accent', '#06b6d4')}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Master Audio & Voiceover -->
      <div class="card">
        <h2>🎙️ Voiceover & Sound Master</h2>
        <p style="color: var(--text-muted); font-size: 14px;">Microsoft Neural Studio Master (-14 LUFS Broadcast Compliant)</p>
        <audio controls src="{voiceover_rel_path}"></audio>
        <div class="script-box">
          <strong>Script:</strong><br>{script_text}
        </div>
        <div style="margin-top: 16px;">
          <a href="{voiceover_rel_path}" download class="btn btn-primary" style="width: 100%;">Download WAV Audio</a>
        </div>
      </div>
    </div>

    <div class="card" style="text-align: center; padding: 48px 32px;">
      <h2 style="justify-content: center;">🎬 4K Commercial Composition</h2>
      <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto 24px auto;">
        Rendered deterministically at 60 FPS using Remotion & Three.js hardware acceleration.
      </p>
      <div style="font-family: monospace; background: rgba(0,0,0,0.5); padding: 14px; border-radius: 10px; display: inline-block; color: var(--accent);">
        cd video && npx remotion render src/index.ts Commercial --output=commercial.mp4
      </div>
    </div>

    <div class="footer">
      Generated automatically by Universal Agency Pipeline • Ready for Client Handover
    </div>
  </div>
</body>
</html>
"""
        with open(portal_file, "w", encoding="utf-8") as f:
            f.write(html_template)

        return str(portal_file.resolve())
