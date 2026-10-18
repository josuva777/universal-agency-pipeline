import os
import json
import asyncio
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

class GCSUploadResult(BaseModel):
    file_path: str
    public_url: str
    bucket_name: str
    bytes_uploaded: int
    content_type: str
    mempalace_saved: bool

class GoogleCloudStorageUploader:
    """Uploads videos, audio tracks, and assets to Google Cloud Storage (GCS)

    and files the permanent link into MemPalace for instant semantic recall.
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
        bucket_name: Optional[str] = None
    ) -> GCSUploadResult:
        file = Path(local_file_path).resolve()
        if not file.exists():
            raise FileNotFoundError(f"File not found: {local_file_path}")

        file_bytes = file.stat().st_size
        content_type = cls.get_content_type(file)
        target_bucket = bucket_name or os.getenv("GCS_BUCKET_NAME", "agency-media-bucket")
        destination_blob_name = f"{project_name.lower().replace(' ', '_')}/{file.name}"

        public_url = f"file:///{file.as_posix()}"
        uploaded_to_gcs = False

        # Check for Google Cloud credentials
        gcs_creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if gcs_creds_path and Path(gcs_creds_path).exists():
            try:
                from google.cloud import storage
                client = storage.Client.from_service_account_json(gcs_creds_path)
                bucket = client.bucket(target_bucket)
                blob = bucket.blob(destination_blob_name)
                blob.upload_from_filename(str(file), content_type=content_type)
                
                # Make publicly readable or use public URL format
                public_url = f"https://storage.googleapis.com/{target_bucket}/{destination_blob_name}"
                uploaded_to_gcs = True
            except Exception as e:
                print(f"[Warning] GCS upload fallback to local: {e}")

        # Record into MemPalace memory
        saved_to_mempalace = False
        try:
            mempalace_record = {
                "project": project_name,
                "asset_name": file.name,
                "public_url": public_url,
                "storage_provider": "google_cloud_storage" if uploaded_to_gcs else "local_disk",
                "file_size_bytes": file_bytes,
                "timestamp": "2026-10-18"
            }
            mem_dir = Path("C:/Users/ELCOT/.gemini/antigravity/scratch/agency-workspace/.agents/memory")
            mem_dir.mkdir(parents=True, exist_ok=True)
            mem_file = mem_dir / "project_assets_memory.jsonl"
            with open(mem_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(mempalace_record) + "\n")
            saved_to_mempalace = True
        except Exception:
            pass

        return GCSUploadResult(
            file_path=str(file),
            public_url=public_url,
            bucket_name=target_bucket,
            bytes_uploaded=file_bytes,
            content_type=content_type,
            mempalace_saved=saved_to_mempalace
        )

if __name__ == "__main__":
    test_path = "C:/Users/ELCOT/.gemini/antigravity/scratch/creative-agent-studio/assets/outputs/smoke_test.mp4"
    if Path(test_path).exists():
        res = asyncio.run(GoogleCloudStorageUploader.upload_asset(test_path, "SmokeTest"))
        print("GCS Result:", res.model_dump())
