import os
import httpx
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class BRollClip(BaseModel):
    id: str
    url: str
    local_path: Optional[str] = None
    duration_seconds: float
    width: int
    height: int
    source: str

class BRollFetcher:
    """Fetches high-definition, royalty-free 4K/HD video b-roll from Pexels & Pixabay ($0 free tiers)."""

    CACHE_DIR = Path("C:/Users/ELCOT/.gemini/antigravity/scratch/creative-agent-studio/assets/broll_cache")
    VEO_LOCAL_DIR = Path("C:/Users/ELCOT/.gemini/antigravity/scratch/creative-agent-studio/assets/broll")
    VEO_GDRIVE_DIR = Path("G:/My Drive/Agency Deliverables/veo_broll")

    def __init__(self):
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        self.pixabay_key = os.getenv("PIXABAY_API_KEY")
        self.custom_veo_dir = os.getenv("VEO_BROLL_DIR")
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.VEO_LOCAL_DIR.mkdir(parents=True, exist_ok=True)

    async def search_clips(self, query: str, count: int = 3) -> List[BRollClip]:
        clips: List[BRollClip] = []

        # 0. Priority: Check Custom / Google Veo 3.1 AI Video Folders
        scan_paths = []
        if self.custom_veo_dir and Path(self.custom_veo_dir).exists():
            scan_paths.append(Path(self.custom_veo_dir))
        if self.VEO_GDRIVE_DIR.exists():
            scan_paths.append(self.VEO_GDRIVE_DIR)
        if self.VEO_LOCAL_DIR.exists():
            scan_paths.append(self.VEO_LOCAL_DIR)

        for scan_dir in scan_paths:
            for ext in ("*.mp4", "*.mov", "*.webm"):
                for video_file in scan_dir.glob(ext):
                    if len(clips) >= count:
                        break
                    clips.append(BRollClip(
                        id=video_file.stem,
                        url=str(video_file.resolve()),
                        local_path=str(video_file.resolve()),
                        duration_seconds=5.0,
                        width=1920,
                        height=1080,
                        source="veo_ai"
                    ))
            if len(clips) >= count:
                return clips[:count]

        # 1. Pexels API (High-quality 4K commercial footage)
        if self.pexels_key and self.pexels_key != "your_pexels_api_key_here":
            try:
                headers = {"Authorization": self.pexels_key}
                url = f"https://api.pexels.com/videos/search?query={query}&per_page={count}&orientation=landscape"
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        for video in data.get("videos", []):
                            # Select highest resolution video file
                            video_files = video.get("video_files", [])
                            best_file = max(video_files, key=lambda x: x.get("width", 0), default=None)
                            if best_file:
                                clips.append(BRollClip(
                                    id=str(video["id"]),
                                    url=best_file["link"],
                                    duration_seconds=float(video.get("duration", 5)),
                                    width=best_file.get("width", 1920),
                                    height=best_file.get("height", 1080),
                                    source="pexels"
                                ))
            except Exception as e:
                print(f"[Warning] Pexels search failed: {e}")

        # 2. Pixabay API Fallback
        if len(clips) < count and self.pixabay_key and self.pixabay_key != "your_pixabay_key_here":
            try:
                url = f"https://pixabay.com/api/videos/?key={self.pixabay_key}&q={query}&per_page={count}"
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        data = resp.json()
                        for hit in data.get("hits", []):
                            large_vid = hit.get("videos", {}).get("large", {})
                            if large_vid:
                                clips.append(BRollClip(
                                    id=str(hit["id"]),
                                    url=large_vid["url"],
                                    duration_seconds=float(hit.get("duration", 5)),
                                    width=large_vid.get("width", 1920),
                                    height=large_vid.get("height", 1080),
                                    source="pixabay"
                                ))
            except Exception as e:
                print(f"[Warning] Pixabay search failed: {e}")

        return clips[:count]

    async def download_clip(self, clip: BRollClip) -> str:
        """Downloads clip to local cache."""
        target_file = self.CACHE_DIR / f"{clip.source}_{clip.id}.mp4"
        if target_file.exists():
            clip.local_path = str(target_file.resolve())
            return clip.local_path

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(clip.url)
            if resp.status_code == 200:
                with open(target_file, "wb") as f:
                    f.write(resp.content)
                clip.local_path = str(target_file.resolve())
                return clip.local_path

        return clip.url

