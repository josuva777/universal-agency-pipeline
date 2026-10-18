import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel

class MediaUploadResult(BaseModel):
    file_path: str
    media_url: str
    storage_provider: str  # "cloudflare_r2" or "local"
    bytes_uploaded: int
    content_type: str
    mempalace_saved: bool

class CloudflareR2Uploader:
    """Uploads videos, audio masters, and brand assets to Cloudflare R2 ($0 free 10GB tier, zero egress fees)

    and saves the permanent link into MemPalace for instant recall across any agent or session.
    """

    @classmethod
    def get_content_type(cls, file_path: Path) -> str:
        ext = file_path.suffix.lower()
        mapping = {
            ".mp4": "video/mp4",
            ".wav": "audio/wav",
            ".mp3": "audio/mpeg",
            ".svg": "image/svg+xml",
            ".png": "image/png",
            ".html": "text/html",
            ".json": "application/json",
            ".srt": "text/plain",
        }
        return mapping.get(ext, "application/octet-stream")

    @classmethod
    async def upload_asset(
        cls,
        local_file_path: str,
        project_name: str,
        custom_key: Optional[str] = None
    ) -> MediaUploadResult:
        file = Path(local_file_path).resolve()
        if not file.exists():
            raise FileNotFoundError(f"File not found: {local_file_path}")

        file_bytes = file.stat().st_size
        content_type = cls.get_content_type(file)
        object_key = custom_key or f"{project_name.lower().replace(' ', '_')}/{file.name}"

        # Cloudflare R2 environment variables
        account_id = os.getenv("CLOUDFLARE_R2_ACCOUNT_ID")
        access_key = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
        secret_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        bucket_name = os.getenv("CLOUDFLARE_R2_BUCKET_NAME", "agency-media")
        public_domain = os.getenv("CLOUDFLARE_R2_PUBLIC_DOMAIN")  # e.g., "https://media.myagency.com" or r2.dev

        uploaded_to_r2 = False
        final_url = f"file:///{file.as_posix()}"

        # 1. Upload to Cloudflare R2 via boto3 / httpx if credentials present
        if account_id and access_key and secret_key and access_key != "your_r2_access_key":
            try:
                import boto3
                endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"
                s3_client = boto3.client(
                    "s3",
                    endpoint_url=endpoint_url,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    region_name="auto"
                )
                with open(file, "rb") as f:
                    s3_client.put_object(
                        Bucket=bucket_name,
                        Key=object_key,
                        Body=f,
                        ContentType=content_type
                    )
                if public_domain:
                    final_url = f"{public_domain.rstrip('/')}/{object_key}"
                else:
                    final_url = f"https://{bucket_name}.{account_id}.r2.cloudflarestorage.com/{object_key}"
                uploaded_to_r2 = True
            except Exception as e:
                print(f"[Warning] Cloudflare R2 upload fallback to local: {e}")

        # 2. Record Permanent Asset into MemPalace Memory
        saved_to_mempalace = False
        try:
            from pathlib import Path
            mempalace_record = {
                "project": project_name,
                "asset_name": file.name,
                "media_url": final_url,
                "file_size_bytes": file_bytes,
                "storage": "cloudflare_r2" if uploaded_to_r2 else "local_disk",
                "timestamp": "2026-10-18"
            }
            # Save into memory drawer log
            mem_dir = Path("C:/Users/ELCOT/.gemini/antigravity/scratch/agency-workspace/.agents/memory")
            mem_dir.mkdir(parents=True, exist_ok=True)
            mem_file = mem_dir / "project_assets_memory.jsonl"
            with open(mem_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(mempalace_record) + "\n")
            saved_to_mempalace = True
        except Exception:
            pass

        return MediaUploadResult(
            file_path=str(file),
            media_url=final_url,
            storage_provider="cloudflare_r2" if uploaded_to_r2 else "local",
            bytes_uploaded=file_bytes,
            content_type=content_type,
            mempalace_saved=saved_to_mempalace
        )

if __name__ == "__main__":
    test_file = "C:/Users/ELCOT/.gemini/antigravity/scratch/creative-agent-studio/assets/outputs/smoke_test.mp4"
    if Path(test_file).exists():
        res = asyncio.run(CloudflareR2Uploader.upload_asset(test_file, "SmokeTest"))
        print("Upload result:", res.model_dump())
