from fastapi import UploadFile
from pathlib import Path
import shutil
import uuid
import re
from app.settings import Settings

settings = Settings()


UPLOAD_DIR = Path(f"{settings.ASSETS_FOLDER_PATH}/product_imgs")
print("🚀 UPLOAD_DIR =", UPLOAD_DIR.resolve())

print("🚀 settings.ASSETS_FOLDER_PATH =", settings.ASSETS_FOLDER_PATH)
print("🚀 settings.ASYNC_DATABASE_URL =", settings.ASYNC_DATABASE_URL)
print("🚀 settings.SYNC_DATABASE_URL =", settings.SYNC_DATABASE_URL)

# inner folder path
# UPLOAD_DIR = Path("app/uploads/product_imgs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def img_uploader(img: UploadFile) -> str | None:

    if img:
        # Extract original file extension
        ext = Path(img.filename).suffix

        # Remove unsafe characters from filename (keep only letters, numbers, _, -, .)
        safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", Path(img.filename).stem)

        # Add unique prefix using UUID
        unique_name = f"{uuid.uuid4().hex}_{safe_name}{ext}"

        # Full path on disk
        file_path = UPLOAD_DIR / unique_name

        print("📝 FINAL SAVE PATH =", file_path.resolve())
        print("📝 WORKING DIR =", Path().resolve())

        # Save file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

        print("✅ SAVED EXISTS:", file_path.exists(), "AT:", file_path.resolve())

        # Return public path for URL
        image_path = f"/uploads/product_imgs/{unique_name}"

        return image_path
    else:
        return None


def delete_image(image_path: str):
    if not image_path:
        return

    # image_path looks like: /uploads/product_imgs/xxxxx.png
    try:
        filename = Path(image_path).name
        file_path = UPLOAD_DIR / filename
    except Exception:
        return

    if file_path.exists():
        file_path.unlink()
        print(f"Deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")
