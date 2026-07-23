from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from auth.dependencies import get_current_user
from database.mongodb import documents_collection

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):

    allowed_extensions = {
        ".pdf",
        ".docx",
        ".txt"
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    user_id = str(current_user["_id"])

    user_folder = UPLOAD_DIR / user_id
    user_folder.mkdir(parents=True, exist_ok=True)

    file_path = user_folder / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    document = {
        "user_id": user_id,
        "filename": file.filename,
        "filepath": str(file_path),
        "file_size": file_path.stat().st_size,
        "content_type": file.content_type,
        "uploaded_at": datetime.utcnow()
    }

    result = documents_collection.insert_one(document)

    return {
        "message": "File uploaded successfully",
        "document_id": str(result.inserted_id),
        "filename": file.filename
    }
@router.get("/")
def list_documents(
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    documents = documents_collection.find(
        {
            "user_id": user_id
        }
    )

    result = []

    for doc in documents:

        result.append({

            "id": str(doc["_id"]),

            "filename": doc["filename"],

            "file_size": doc["file_size"],

            "content_type": doc["content_type"],

            "uploaded_at": doc["uploaded_at"]

        })

    return result