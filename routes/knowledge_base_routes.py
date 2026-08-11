from pydantic import BaseModel
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from auth.dependencies import get_current_user

from database.mongodb import knowledge_base_collection

from models.knowledge_base_model import CreateKnowledgeBase

from services.knowledge_base_service import (
    create_knowledge_base,
    get_knowledge_base
)

router = APIRouter()

UPLOAD_DIR = Path("uploads")

class CreateKnowledgeBase(BaseModel):
    name: str
    description: str | None = None

@router.post("/")
def create_knowledge_base(
    data: CreateKnowledgeBase,
    current_user=Depends(get_current_user)
):
    user_id = str(current_user["_id"])

    # Prevent duplicate KB names for the same user
    existing = knowledge_base_collection.find_one({
        "user_id": user_id,
        "name": data.name
    })

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Knowledge base with this name already exists."
        )

    kb = {
        "user_id": user_id,
        "name": data.name,
        "description": data.description,
        "created_at": datetime.utcnow()
    }

    result = knowledge_base_collection.insert_one(kb)

    kb_id = str(result.inserted_id)

    kb_folder = UPLOAD_DIR / user_id / f"kb_{kb_id}"
    kb_folder.mkdir(parents=True, exist_ok=True)

    return {
        "message": "Knowledge base created successfully",
        "knowledge_base_id": kb_id,
        "name": data.name,
        "description": data.description
    }

@router.post("/")
def create_knowledge_base_route(
    data: CreateKnowledgeBase,
    current_user=Depends(get_current_user)
):

    return create_knowledge_base(
        data,
        current_user
    )
@router.get("/")
def list_knowledge_bases(
    current_user=Depends(get_current_user)
):

    return get_knowledge_base(current_user)

@router.get("/{knowledge_base_id}")
def get_knowledge_base_route(
    knowledge_base_id: str,
    current_user=Depends(get_current_user)
):

    return get_knowledge_base(
        knowledge_base_id,
        current_user
    )