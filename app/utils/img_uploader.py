from fastapi import UploadFile
from pathlib import Path
import shutil
import uuid


UPLOAD_DIR = Path("app/uploads/product_imgs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def img_uploader(img: UploadFile) -> str | None:

    if img:
        unique_name = f"{uuid.uuid4().hex}_{img.filename}"
        file_path = UPLOAD_DIR / unique_name

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

        image_path = f"/uploads/product_imgs/{unique_name}"

        return image_path
    else:
        return None
