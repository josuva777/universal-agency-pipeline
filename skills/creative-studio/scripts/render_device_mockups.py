#!/usr/bin/env python3
"""
Hollywood 3D Device Mockup Asset Generator
Procedural 3D device frames (SVG vector + Interactive Three.js 3D HTML)
Supports: iPhone 16 Pro, MacBook Pro 16", Apple Studio Display
Palettes: Clay Minimal, Cyber Metallic, Titanium Pro
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEVICE_CONFIGS = {
    "iphone16pro": {
        "name": "iPhone 16 Pro",
        "width": 440,
        "height": 900,
        "screen_x": 22,
        "screen_y": 20,
        "screen_w": 396,
        "screen_h": 860,
        "radius": 56,
        "screen_radius": 46,
        "island_w": 126,
        "island_h": 36,
        "island_y": 32,
    },
    "macbookpro": {
        "name": "MacBook Pro 16",
        "width": 1080,
        "height": 720,
        "screen_x": 100,
        "screen_y": 50,
        "screen_w": 880,
        "screen_h": 550,
        "radius": 24,
        "screen_radius": 12,
        "notch_w": 180,
        "notch_h": 28,
    },
    "studiodisplay": {
        "name": "Studio Display",
        "width": 1200,
        "height": 880,
        "screen_x": 60,
        "screen_y": 60,
        "screen_w": 1080,
        "screen_h": 608,
        "radius": 28,
        "screen_radius": 14,
    }
}

PALETTES = {
    "cyber": {
        "body_fill": "url(#cyberBodyGrad)",
        "bezel_stroke": "#10b981",
        "bezel_glow": "rgba(16, 185, 129, 0.4)",
        "accent": "#059669",
        "screen_bg": "#0a0f1d",
        "reflection_opacity": "0.15",
        "shadow_color": "rgba(0, 0, 0, 0.8)",
        "text_color": "#10b981",
    },
    "titanium": {
        "body_fill": "url(#titaniumBodyGrad)",
        "bezel_stroke": "#64748b",
        "bezel_glow": "rgba(148, 163, 184, 0.25)",
        "accent": "#38bdf8",
        "screen_bg": "#020617",
        "reflection_opacity": "0.12",
        "shadow_color": "rgba(0, 0, 0, 0.75)",
        "text_color": "#f8fafc",
    },
    "clay": {
        "body_fill": "url(#clayBodyGrad)",
        "bezel_stroke": "#cbd5e1",
        "bezel_glow": "rgba(203, 213, 225, 0.2)",
        "accent": "#6366f1",
        "screen_bg": "#f8fafc",
        "reflection_opacity": "0.08",
        "shadow_color": "rgba(15, 23, 42, 0.12)",
        "text_color": "#0f172a",
    }
}

def generate_iphone_svg(style: str = "cyber", screen_img: Optional[str] = None) -> str:
    cfg = DEVICE_CONFIGS["iphone16pro"]
    p = PALETTES.get(style, PALETTES["cyber"])
    
    screen_content = ""
    if screen_img:
        screen_content = f'''<image href="{screen_img}" x="{cfg['screen_x']}" y="{cfg['screen_y']}" width="{cfg['screen_w']}" height="{cfg['screen_h']}" preserveAspectRatio="xMidYMid slice" clip-path="url(#iphoneScreenClip)"/>'''
    else:
        screen_content = f'''
        <rect x="{cfg['screen_x']}" y="{cfg['screen_y']}" width="{cfg['screen_w']}" height="{cfg['screen_h']}" rx="{cfg['screen_radius']}" fill="{p['screen_bg']}"/>
        <!-- Default Live Interface Mockup -->
        <g clip-path="url(#iphoneScreenClip)">
            <!-- Header bar -->
            <rect x="40" y="80" width="180" height="24" rx="6" fill="{p['bezel_stroke']}" fill-opacity="0.2"/>
            <circle cx="390" cy="92" r="14" fill="{p['accent']}" fill-opacity="0.6"/>
            <!-- Hero Card -->
            <rect x="40" y="140" width="360" height="200" rx="18" fill="#1e293b" stroke="{p['bezel_stroke']}" stroke-width="1.5" stroke-opacity="0.4"/>
            <text x="60" y="190" fill="{p['text_color']}" font-family="system-ui, sans-serif" font-size="20" font-weight="700">SentinelOps Guard</text>
            <text x="60" y="222" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="13">Autonomous Agent Fleet · Active</text>
            <rect x="60" y="250" width="130" height="36" rx="8" fill="{p['accent']}"/>
            <text x="96" y="274" fill="#ffffff" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Deploy</text>
            <!-- Data Grid Rows -->
            <rect x="40" y="370" width="360" height="90" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1"/>
            <rect x="40" y="480" width="360" height="90" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1"/>
            <rect x="40" y="590" width="360" height="90" rx="14" fill="#0f172a" stroke="#334155" stroke-width="1"/>
        </g>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cfg['width'] + 60} {cfg['height'] + 60}" width="{cfg['width'] + 60}" height="{cfg['height'] + 60}">
  <defs>
    <!-- Gradients -->
    <linearGradient id="cyberBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <linearGradient id="titaniumBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#475569"/>
      <stop offset="50%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
    <linearGradient id="clayBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="50%" stop-color="#f1f5f9"/>
      <stop offset="100%" stop-color="#e2e8f0"/>
    </linearGradient>
    <linearGradient id="glareGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="{p['reflection_opacity']}"/>
      <stop offset="40%" stop-color="#ffffff" stop-opacity="0.0"/>
    </linearGradient>
    <!-- Drop Shadow Filter -->
    <filter id="phoneShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="24" stdDeviation="32" flood-color="{p['shadow_color']}"/>
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="{p['bezel_glow']}"/>
    </filter>
    <clipPath id="iphoneScreenClip">
      <rect x="{cfg['screen_x']}" y="{cfg['screen_y']}" width="{cfg['screen_w']}" height="{cfg['screen_h']}" rx="{cfg['screen_radius']}"/>
    </clipPath>
  </defs>

  <g transform="translate(30, 20)">
    <!-- Outer Shadow and Body Frame -->
    <rect x="0" y="0" width="{cfg['width']}" height="{cfg['height']}" rx="{cfg['radius']}" fill="{p['body_fill']}" stroke="{p['bezel_stroke']}" stroke-width="3" filter="url(#phoneShadow)"/>
    
    <!-- Outer Buttons (Volume & Power) -->
    <rect x="-4" y="160" width="4" height="48" rx="2" fill="{p['bezel_stroke']}"/>
    <rect x="-4" y="225" width="4" height="48" rx="2" fill="{p['bezel_stroke']}"/>
    <rect x="{cfg['width']}" y="190" width="4" height="72" rx="2" fill="{p['bezel_stroke']}"/>

    <!-- Screen Bezel Border -->
    <rect x="{cfg['screen_x'] - 2}" y="{cfg['screen_y'] - 2}" width="{cfg['screen_w'] + 4}" height="{cfg['screen_h'] + 4}" rx="{cfg['screen_radius'] + 2}" fill="none" stroke="#000000" stroke-width="4"/>

    <!-- Screen Content -->
    {screen_content}

    <!-- Dynamic Island -->
    <rect x="{(cfg['width'] - cfg['island_w']) // 2}" y="{cfg['island_y']}" width="{cfg['island_w']}" height="{cfg['island_h']}" rx="18" fill="#000000"/>
    <circle cx="{(cfg['width'] - cfg['island_w']) // 2 + 30}" cy="{cfg['island_y'] + 18}" r="5.5" fill="#1e1e1e"/>
    <circle cx="{(cfg['width'] - cfg['island_w']) // 2 + cfg['island_w'] - 28}" cy="{cfg['island_y'] + 18}" r="4.5" fill="#0b1b3a"/>

    <!-- Glass Glare Reflection -->
    <path d="M {cfg['screen_x']} {cfg['screen_y']} L {cfg['screen_x'] + cfg['screen_w']} {cfg['screen_y']} L {cfg['screen_x']} {cfg['screen_y'] + cfg['screen_h'] // 2} Z" fill="url(#glareGrad)" clip-path="url(#iphoneScreenClip)"/>
  </g>
</svg>'''
    return svg

def generate_macbook_svg(style: str = "cyber", screen_img: Optional[str] = None) -> str:
    cfg = DEVICE_CONFIGS["macbookpro"]
    p = PALETTES.get(style, PALETTES["cyber"])
    
    screen_content = ""
    if screen_img:
        screen_content = f'''<image href="{screen_img}" x="{cfg['screen_x']}" y="{cfg['screen_y']}" width="{cfg['screen_w']}" height="{cfg['screen_h']}" preserveAspectRatio="xMidYMid slice" clip-path="url(#macScreenClip)"/>'''
    else:
        screen_content = f'''
        <rect x="{cfg['screen_x']}" y="{cfg['screen_y']}" width="{cfg['screen_w']}" height="{cfg['screen_h']}" rx="{cfg['screen_radius']}" fill="{p['screen_bg']}"/>
        <g clip-path="url(#macScreenClip)">
          <!-- Top Window Controls -->
          <circle cx="{cfg['screen_x'] + 24}" cy="{cfg['screen_y'] + 24}" r="6" fill="#ef4444"/>
          <circle cx="{cfg['screen_x'] + 44}" cy="{cfg['screen_y'] + 24}" r="6" fill="#f59e0b"/>
          <circle cx="{cfg['screen_x'] + 64}" cy="{cfg['screen_y'] + 24}" r="6" fill="#10b981"/>
          <!-- Dashboard Sidebar -->
          <rect x="{cfg['screen_x']}" y="{cfg['screen_y'] + 48}" width="200" height="{cfg['screen_h'] - 48}" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
          <!-- Dashboard Main Area -->
          <text x="{cfg['screen_x'] + 240}" y="{cfg['screen_y'] + 100}" fill="{p['text_color']}" font-family="system-ui, sans-serif" font-size="28" font-weight="700">Universal Agency Pipeline v2.1</text>
          <text x="{cfg['screen_x'] + 240}" y="{cfg['screen_y'] + 135}" fill="#64748b" font-family="system-ui, sans-serif" font-size="16">Autonomous Verification Matrix · 12/12 Green</text>
          <!-- Metric Cards -->
          <rect x="{cfg['screen_x'] + 240}" y="{cfg['screen_y'] + 170}" width="180" height="100" rx="12" fill="#1e293b"/>
          <rect x="{cfg['screen_x'] + 450}" y="{cfg['screen_y'] + 170}" width="180" height="100" rx="12" fill="#1e293b"/>
          <rect x="{cfg['screen_x'] + 660}" y="{cfg['screen_y'] + 170}" width="180" height="100" rx="12" fill="#1e293b"/>
          <!-- Terminal preview box -->
          <rect x="{cfg['screen_x'] + 240}" y="{cfg['screen_y'] + 300}" width="600" height="200" rx="12" fill="#020617" stroke="#334155" stroke-width="1"/>
          <text x="{cfg['screen_x'] + 260}" y="{cfg['screen_y'] + 340}" fill="{p['bezel_stroke']}" font-family="monospace" font-size="14">$ uap verify --security --all</text>
          <text x="{cfg['screen_x'] + 260}" y="{cfg['screen_y'] + 375}" fill="#10b981" font-family="monospace" font-size="14">[✓] OWASP Top 10 Guardrails: 0 Violations</text>
          <text x="{cfg['screen_x'] + 260}" y="{cfg['screen_y'] + 410}" fill="#10b981" font-family="monospace" font-size="14">[✓] CycloneDX SBOM: Cryptographically Signed</text>
        </g>
        '''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cfg['width'] + 60} {cfg['height'] + 60}" width="{cfg['width'] + 60}" height="{cfg['height'] + 60}">
  <defs>
    <filter id="macShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="30" stdDeviation="35" flood-color="{p['shadow_color']}"/>
      <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="{p['bezel_glow']}"/>
    </filter>
    <clipPath id="macScreenClip">
      <rect x="{cfg['screen_x']}" y="{cfg['screen_y']}" width="{cfg['screen_w']}" height="{cfg['screen_h']}" rx="{cfg['screen_radius']}"/>
    </clipPath>
  </defs>

  <g transform="translate(30, 20)">
    <!-- Display Lid -->
    <rect x="80" y="30" width="920" height="590" rx="{cfg['radius']}" fill="#0f172a" stroke="{p['bezel_stroke']}" stroke-width="3" filter="url(#macShadow)"/>
    
    <!-- Screen Viewport -->
    {screen_content}

    <!-- Camera Notch -->
    <rect x="{(1080 - cfg['notch_w']) // 2}" y="{cfg['screen_y']}" width="{cfg['notch_w']}" height="{cfg['notch_h']}" rx="8" fill="#0f172a"/>
    <circle cx="{1080 // 2}" cy="{cfg['screen_y'] + 14}" r="4" fill="#020617"/>

    <!-- Unibody Bottom Base -->
    <path d="M 20 620 L 1060 620 L 1020 645 L 60 645 Z" fill="#1e293b" stroke="{p['bezel_stroke']}" stroke-width="1.5"/>
    <rect x="470" y="620" width="140" height="8" rx="4" fill="#334155"/>
  </g>
</svg>'''
    return svg

def generate_interactive_3d_html(style: str = "cyber", out_path: Path = Path("mockup_3d.html")) -> None:
    p = PALETTES.get(style, PALETTES["cyber"])
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hollywood 3D Device Studio Mockup</title>
  <style>
    body {{
      margin: 0;
      background: #020617;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}
    #canvas-container {{
      width: 100vw;
      height: 100vh;
    }}
    .ui-panel {{
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(12px);
      padding: 12px 24px;
      border-radius: 9999px;
      display: flex;
      gap: 16px;
      align-items: center;
      z-index: 10;
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }}
    button {{
      background: #1e293b;
      color: #f8fafc;
      border: 1px solid #334155;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      font-size: 13px;
      transition: all 0.2s ease;
    }}
    button:hover {{
      background: #334155;
      border-color: {p['bezel_stroke']};
      color: {p['bezel_stroke']};
    }}
    .active {{
      background: {p['bezel_stroke']};
      color: #020617;
      border-color: {p['bezel_stroke']};
    }}
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
  <div id="canvas-container"></div>
  <div class="ui-panel">
    <button id="btn-rotate" class="active">Auto Orbit: ON</button>
    <button id="btn-clay">Clay Matte</button>
    <button id="btn-cyber">Cyber Emerald</button>
    <button id="btn-titanium">Titanium Blue</button>
    <button id="btn-export">Export Canvas PNG</button>
  </div>

  <script>
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x020617, 0.05);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.set(0, 0, 8);

    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, preserveDrawingBuffer: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Lighting Setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 2.0);
    keyLight.position.set(5, 5, 5);
    keyLight.castShadow = true;
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0x10b981, 3.0);
    rimLight.position.set(-5, -3, -4);
    scene.add(rimLight);

    // Device Mesh Group
    const deviceGroup = new THREE.Group();
    scene.add(deviceGroup);

    // Phone Body Geometry
    const bodyGeometry = new THREE.BoxGeometry(2.4, 4.9, 0.28);
    const bodyMaterial = new THREE.MeshStandardMaterial({{
      color: 0x0f172a,
      metalness: 0.85,
      roughness: 0.25
    }});
    const phoneBody = new THREE.Mesh(bodyGeometry, bodyMaterial);
    phoneBody.castShadow = true;
    phoneBody.receiveShadow = true;
    deviceGroup.add(phoneBody);

    // Screen Geometry
    const screenGeometry = new THREE.PlaneGeometry(2.25, 4.75);
    const screenMaterial = new THREE.MeshBasicMaterial({{ color: 0x020617 }});
    const phoneScreen = new THREE.Mesh(screenGeometry, screenMaterial);
    phoneScreen.position.z = 0.145;
    deviceGroup.add(phoneScreen);

    // Glow Halo Edge
    const haloGeo = new THREE.RingGeometry(2.5, 2.65, 32);
    const haloMat = new THREE.MeshBasicMaterial({{ color: 0x10b981, side: THREE.DoubleSide, transparent: true, opacity: 0.2 }});
    const halo = new THREE.Mesh(haloGeo, haloMat);
    halo.position.z = -0.15;
    deviceGroup.add(halo);

    // Animation Loop
    let autoRotate = true;
    function animate() {{
      requestAnimationFrame(animate);
      if (autoRotate) {{
        deviceGroup.rotation.y += 0.008;
      }}
      controls.update();
      renderer.render(scene, camera);
    }}
    animate();

    // UI Buttons
    const btnRotate = document.getElementById('btn-rotate');
    btnRotate.onclick = () => {{
      autoRotate = !autoRotate;
      btnRotate.textContent = 'Auto Orbit: ' + (autoRotate ? 'ON' : 'OFF');
      btnRotate.classList.toggle('active', autoRotate);
    }};

    document.getElementById('btn-clay').onclick = () => {{
      bodyMaterial.color.setHex(0xe2e8f0);
      bodyMaterial.metalness = 0.1;
      bodyMaterial.roughness = 0.8;
      rimLight.color.setHex(0x6366f1);
      haloMat.color.setHex(0x6366f1);
    }};

    document.getElementById('btn-cyber').onclick = () => {{
      bodyMaterial.color.setHex(0x0f172a);
      bodyMaterial.metalness = 0.9;
      bodyMaterial.roughness = 0.2;
      rimLight.color.setHex(0x10b981);
      haloMat.color.setHex(0x10b981);
    }};

    document.getElementById('btn-titanium').onclick = () => {{
      bodyMaterial.color.setHex(0x334155);
      bodyMaterial.metalness = 0.95;
      bodyMaterial.roughness = 0.3;
      rimLight.color.setHex(0x38bdf8);
      haloMat.color.setHex(0x38bdf8);
    }};

    document.getElementById('btn-export').onclick = () => {{
      const link = document.createElement('a');
      link.download = 'device-3d-mockup.png';
      link.href = renderer.domElement.toDataURL('image/png');
      link.click();
    }};

    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});
  </script>
</body>
</html>
'''
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description="Hollywood 3D Device Mockup Asset Generator")
    parser.add_argument("--device", "-d", choices=["iphone16pro", "macbookpro", "studiodisplay", "all"], default="all")
    parser.add_argument("--style", "-s", choices=["cyber", "titanium", "clay"], default="cyber")
    parser.add_argument("--screen", help="Path to image screenshot to embed")
    parser.add_argument("--out-dir", "-o", default="mockups", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 64)
    print("  3D DEVICE MOCKUP ASSET GENERATOR (Procedural Studio Engine)")
    print("=" * 64)
    print(f"[*] Style Palette: {args.style}")
    print(f"[*] Output Directory: {out_dir.resolve()}")

    if args.device in ["iphone16pro", "all"]:
        svg_iphone = generate_iphone_svg(style=args.style, screen_img=args.screen)
        iphone_path = out_dir / f"mockup_iphone16pro_{args.style}.svg"
        iphone_path.write_text(svg_iphone, encoding="utf-8")
        print(f"  [OK] Generated: {iphone_path.name}")

    if args.device in ["macbookpro", "all"]:
        svg_mac = generate_macbook_svg(style=args.style, screen_img=args.screen)
        mac_path = out_dir / f"mockup_macbookpro_{args.style}.svg"
        mac_path.write_text(svg_mac, encoding="utf-8")
        print(f"  [OK] Generated: {mac_path.name}")

    # Generate 3D WebGL Canvas Viewer
    html_3d_path = out_dir / f"studio_3d_viewer_{args.style}.html"
    generate_interactive_3d_html(style=args.style, out_path=html_3d_path)
    print(f"  [OK] Generated: {html_3d_path.name} (Three.js 3D Canvas)")

    print("\n[OK] All 3D Mockup assets successfully generated!")

if __name__ == "__main__":
    main()
