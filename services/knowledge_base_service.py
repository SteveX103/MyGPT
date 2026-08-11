from pathlib import Path
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from database.mongodb import knowledge_base_collection


UPLOAD_DIR = Path("uploads")


def create_knowledge_base(data, current_user):

    user_id = str(current_user["_id"])

    # Check whether this user already has a KB with the same name
    existing = knowledge_base_collection.find_one({
        "user_id": user_id,
        "name": data.name
    })

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Knowledge base with this name already exists."
        )

    # Create knowledge base document
    knowledge_base = {
        "user_id": user_id,
        "name": data.name,
        "description": data.description,
        "created_at": datetime.utcnow()
    }

    result = knowledge_base_collection.insert_one(
        knowledge_base
    )

    knowledge_base_id = str(result.inserted_id)

    # Create user's KB directory
    kb_folder = (
        UPLOAD_DIR
        / user_id
        / f"kb_{knowledge_base_id}"
    )

    kb_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return {
        "message": "Knowledge base created successfully",
        "knowledge_base_id": knowledge_base_id,
        "name": data.name,
        "description": data.description
    }
def get_knowledge_base(
    knowledge_base_id: str,
    current_user
):
    user_id = str(current_user["_id"])

    try:
        kb_object_id = ObjectId(knowledge_base_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid knowledge base ID"
        )

    knowledge_base = knowledge_base_collection.find_one({
        "_id": kb_object_id,
        "user_id": user_id
    })

    if knowledge_base is None:
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not found"
        )

    return {
        "id": str(knowledge_base["_id"]),
        "name": knowledge_base["name"],
        "description": knowledge_base.get("description"),
        "created_at": knowledge_base["created_at"]
    }

