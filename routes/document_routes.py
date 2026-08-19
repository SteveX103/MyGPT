import os
from pathlib import Path
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from auth.dependencies import get_current_user
from database.mongodb import documents_collection
from models.document_model import RenameDocument
from auth.dependencies import get_current_user

from database.mongodb import (
    documents_collection,
    knowledge_base_collection
)
router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.post("/upload")
async def upload_document(
    knowledge_base_id: str = Form(...),
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):

    user_id = str(current_user["_id"])

    # Validate file extension
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

    # Validate Knowledge Base ID
    try:
        kb_object_id = ObjectId(knowledge_base_id)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid knowledge base ID"
        )

    # Verify that the KB belongs to the logged-in user
    knowledge_base = knowledge_base_collection.find_one({
        "_id": kb_object_id,
        "user_id": user_id
    })

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    # Create KB-specific folder
    kb_folder = (
        UPLOAD_DIR
        / user_id
        / f"kb_{knowledge_base_id}"
    )

    kb_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # Generate unique stored filename
    stored_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = kb_folder / stored_filename

    # Save physical file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Store metadata
    document = {
        "user_id": user_id,
        "knowledge_base_id": knowledge_base_id,

        "original_filename": file.filename,
        "stored_filename": stored_filename,

        "filepath": str(file_path),

        "file_size": file_path.stat().st_size,
        "content_type": file.content_type,

        "status": "uploaded",

        "uploaded_at": datetime.utcnow()
    }

    result = documents_collection.insert_one(
        document
    )

    return {
        "message": "File uploaded successfully",
        "document_id": str(result.inserted_id),
        "filename": file.filename,
        "knowledge_base_id": knowledge_base_id
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
    knowledge_base_id: str,
    current_user=Depends(get_current_user)
):
    user_id = str(current_user["_id"])

    # Validate document ID
    try:
        document_object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    # Validate knowledge base ID
    try:
        kb_object_id = ObjectId(knowledge_base_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid knowledge base ID"
        )

    # Verify KB belongs to current user
    knowledge_base = knowledge_base_collection.find_one({
        "_id": kb_object_id,
        "user_id": user_id
    })

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    # Find document inside this KB
    document = documents_collection.find_one({
        "_id": document_object_id,
        "user_id": user_id,
        "knowledge_base_id": knowledge_base_id
    })

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "id": str(document["_id"]),
        "filename": document.get(
            "original_filename",
            document.get("filename")
        ),
        "file_size": document["file_size"],
        "content_type": document["content_type"],
        "status": document.get("status", "uploaded"),
        "uploaded_at": document["uploaded_at"]
    }
@router.get("/{document_id}/download")
def download_document(
    document_id: str,
    knowledge_base_id: str,
    current_user=Depends(get_current_user)
):
    user_id = str(current_user["_id"])

    # Validate document ID
    try:
        document_object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    # Validate knowledge base ID
    try:
        kb_object_id = ObjectId(knowledge_base_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid knowledge base ID"
        )

    # Verify KB ownership
    knowledge_base = knowledge_base_collection.find_one({
        "_id": kb_object_id,
        "user_id": user_id
    })

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    # Find document belonging to this user + KB
    document = documents_collection.find_one({
        "_id": document_object_id,
        "user_id": user_id,
        "knowledge_base_id": knowledge_base_id
    })

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    file_path = Path(document["filepath"])

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Physical file not found"
        )

    original_filename = document.get(
        "original_filename",
        document.get("filename")
    )

    return FileResponse(
        path=str(file_path),
        filename=original_filename,
        media_type=document["content_type"]
    )
@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    knowledge_base_id: str,
    current_user=Depends(get_current_user)
):
    user_id = str(current_user["_id"])

    # Validate document ID
    try:
        document_object_id = ObjectId(document_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    # Validate knowledge base ID
    try:
        kb_object_id = ObjectId(knowledge_base_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid knowledge base ID"
        )

    # Verify KB belongs to current user
    knowledge_base = knowledge_base_collection.find_one({
        "_id": kb_object_id,
        "user_id": user_id
    })

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    # Find document belonging to user + KB
    document = documents_collection.find_one({
        "_id": document_object_id,
        "user_id": user_id,
        "knowledge_base_id": knowledge_base_id
    })

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Delete physical file
    file_path = Path(document["filepath"])

    if file_path.exists():
        file_path.unlink()

    # Delete MongoDB metadata
    documents_collection.delete_one({
        "_id": document_object_id,
        "user_id": user_id,
        "knowledge_base_id": knowledge_base_id
    })

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

