from bson import ObjectId
from fastapi import HTTPException

from database.mongodb import (
    chat_sessions_collection,
    knowledge_base_collection
)


def create_chat_session(
    data,
    current_user
):
    user_id = str(current_user["_id"])

    # Validate KB ID
    try:
        kb_object_id = ObjectId(
            data.knowledge_base_id
        )
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

    chat_session = {
        "user_id": user_id,
        "knowledge_base_id": data.knowledge_base_id,
        "title": data.title,
        "created_at": __import__("datetime").datetime.utcnow(),
        "updated_at": __import__("datetime").datetime.utcnow()
    }

    result = chat_sessions_collection.insert_one(
        chat_session
    )

    return {
        "id": str(result.inserted_id),
        "title": data.title,
        "knowledge_base_id": data.knowledge_base_id,
        "created_at": chat_session["created_at"],
        "updated_at": chat_session["updated_at"]
    }