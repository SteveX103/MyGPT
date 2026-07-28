import os
from pathlib import Path
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from auth.dependencies import get_current_user
from database.mongodb import documents_collection
from models.document_model import RenameDocument

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
@router.get("/{document_id}")
def get_document(
    document_id: str,
    current_user=Depends(get_current_user)
):

    document = documents_collection.find_one(
        {
            "_id": ObjectId(document_id),
            "user_id": str(current_user["_id"])
        }
    ) 

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "id": str(document["_id"]),
        "filename": document["filename"],
        "file_size": document["file_size"],
        "content_type": document["content_type"],
        "uploaded_at": document["uploaded_at"]
    }
@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    current_user=Depends(get_current_user)
):

    document = documents_collection.find_one(
        {
            "_id": ObjectId(document_id),
            "user_id": str(current_user["_id"])
        }
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return FileResponse(
        path=document["filepath"],
        filename=document["filename"],
        media_type=document["content_type"]
    )
@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user=Depends(get_current_user)
):

    document = documents_collection.find_one(
        {
            "_id": ObjectId(document_id),
            "user_id": str(current_user["_id"])
        }
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if os.path.exists(document["filepath"]):
        os.remove(document["filepath"])

    documents_collection.delete_one(
        {
            "_id": ObjectId(document_id)
        }
    )

    return {
        "message": "Document deleted successfully"
    }
@router.put("/{document_id}")
def rename_document(
    document_id: str,
    data: RenameDocument,
    current_user=Depends(get_current_user)
):

    document = documents_collection.find_one(
        {
            "_id": ObjectId(document_id),
            "user_id": str(current_user["_id"])
        }
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    documents_collection.update_one(
        {
            "_id": ObjectId(document_id)
        },
        {
            "$set": {
                "filename": data.filename
            }
        }
    )

    return {
        "message": "Document renamed successfully"
    }