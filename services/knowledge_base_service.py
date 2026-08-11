from pathlib import Path
from datetime import datetime

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
def get_knowledge_bases(current_user):

    user_id = str(current_user["_id"])

    knowledge_bases = knowledge_base_collection.find(
        {
            "user_id": user_id
        }
    ).sort(
        "created_at",
        -1
    )

    result = []

    for kb in knowledge_bases:

        result.append({
            "id": str(kb["_id"]),
            "name": kb["name"],
            "description": kb.get("description"),
            "created_at": kb["created_at"]
        })

    return result