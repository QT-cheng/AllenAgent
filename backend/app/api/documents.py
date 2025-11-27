from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
import shutil

from backend.app.ingestion.loader import load_document
from backend.app.core.config import settings

router = APIRouter(prefix="/documents")


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        allowed_extensions = {".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".jpg", ".png"}
        ext = Path(file.filename).suffix.lower()
        if ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}")
        upload_dir = settings.upload_dir
        upload_dir.mkdir(exist_ok=True)
        safe_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = upload_dir / safe_filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        loaded_files = load_document(file_path)
        return {
            "status": "success",
            "message": f"文档已成功加载到知识库",
            "filename": file.filename,
            "loaded_files": loaded_files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档加载失败: {str(e)}")
