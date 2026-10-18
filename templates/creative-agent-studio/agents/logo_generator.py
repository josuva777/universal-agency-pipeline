from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class BrandPalette(BaseModel):
    primary: str = "#6366f1"
    secondary: str = "#8b5cf6"
    accent: str = "#d946ef"
    background: str = "#0a0b0e"
    surface: str = "#181a20"
    text: str = "#f8fafc"

class LogoGenerator:
    """Generates broadcast-grade procedural SVG vector logos, icons, and wordmarks."""

    @classmethod
    def generate_svg(
        cls,
        brand_name: str,
        tagline: Optional[str] = None,
        style: str = "geometric-hex",
        palette: Optional[BrandPalette] = None,
    ) -> str:
        colors = palette or BrandPalette()
        tag = tagline or "INTELLIGENCE REDEFINED"

        # SVG filter for volumetric metallic glow
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" width="100%" height="100%">
  <defs>
    <linearGradient id="gradBrand" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{colors.primary}" />
      <stop offset="50%" stop-color="{colors.secondary}" />
      <stop offset="100%" stop-color="{colors.accent}" />
    </linearGradient>
    <filter id="glowFilter" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Clean Dark Canvas Shield -->
  <rect width="100%" height="100%" rx="24" fill="{colors.background}" />

  <!-- 1. Geometric Icon Mark -->
  <g transform="translate(60, 50)" filter="url(#glowFilter)">
    <!-- Outer Hexagon Perimeter -->
    <polygon points="100,10 180,55 180,145 100,190 20,145 20,55"
             fill="none"
             stroke="url(#gradBrand)"
             stroke-width="12"
             stroke-linejoin="round"
             stroke-linecap="round" />
    
    <!-- Central Core Node -->
    <circle cx="100" cy="100" r="26" fill="url(#gradBrand)" />
    
    <!-- Isometric Orbit Path -->
    <path d="M 50,75 L 100,100 L 150,75 M 100,100 L 100,160"
          fill="none"
          stroke="{colors.text}"
          stroke-width="4"
          stroke-linecap="round"
          opacity="0.8" />
  </g>

  <!-- 2. Modern Architectural Typography -->
  <g transform="translate(300, 130)">
    <!-- Brand Wordmark -->
    <text x="0" y="0"
          font-family="system-ui, -apple-system, 'Geist Sans', sans-serif"
          font-weight="800"
          font-size="64"
          letter-spacing="-1px"
          fill="{colors.text}">
      {brand_name.upper()}
    </text>

    <!-- Tagline Subtitle -->
    <text x="4" y="44"
          font-family="system-ui, -apple-system, 'Geist Mono', monospace"
          font-weight="600"
          font-size="16"
          letter-spacing="6px"
          fill="{colors.primary}"
          opacity="0.9">
      {tag.upper()}
    </text>
  </g>
</svg>"""
        return svg

    @classmethod
    def save_logo_suite(
        cls,
        brand_name: str,
        output_dir: str,
        tagline: Optional[str] = None,
        palette: Optional[BrandPalette] = None
    ) -> Dict[str, str]:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        svg_content = cls.generate_svg(brand_name, tagline, palette=palette)

        svg_path = out / "logo_master.svg"
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

        return {
            "svg_path": str(svg_path.resolve()),
            "brand_name": brand_name,
        }
