from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

from database.mongodb import (
    chat_sessions_collection,
    chat_messages_collection,
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
def get_user_chat_sessions(current_user):
    user_id = str(current_user["_id"])

    sessions = chat_sessions_collection.find(
        {
            "user_id": user_id
        }
    ).sort(
        "updated_at",
        -1
    )

    result = []

    for session in sessions:

        result.append({
            "id": str(session["_id"]),
            "title": session.get(
                "title",
                "New Chat"
            ),
            "knowledge_base_id": session[
                "knowledge_base_id"
            ],
            "created_at": session.get(
                "created_at"
            ),
            "updated_at": session.get(
                "updated_at"
            )
        })

    return result
def create_chat_message(
    session_id: str,
    data,
    current_user,
    role: str = "user"
):
    user_id = str(current_user["_id"])

    try:
        session_object_id = ObjectId(session_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID"
        )

    # Verify that the session belongs to the logged-in user
    session = chat_sessions_collection.find_one({
        "_id": session_object_id,
        "user_id": user_id
    })

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    if not data.content.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    message = {
        "session_id": session_id,
        "user_id": user_id,
        "role": role,
        "content": data.content.strip(),
        "created_at": datetime.utcnow()
    }

    result = chat_messages_collection.insert_one(
        message
    )

    # Update session activity time
    chat_sessions_collection.update_one(
        {
            "_id": session_object_id
        },
        {
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )

    return {
        "id": str(result.inserted_id),
        "session_id": session_id,
        "role": role,
        "content": message["content"],
        "created_at": message["created_at"]
    }
def get_chat_messages(
    session_id: str,
    current_user
):
    user_id = str(current_user["_id"])

    try:
        session_object_id = ObjectId(session_id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid session ID"
        )

    # Verify session ownership
    session = chat_sessions_collection.find_one({
        "_id": session_object_id,
        "user_id": user_id
    })

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    messages = chat_messages_collection.find(
        {
            "session_id": session_id,
            "user_id": user_id
        }
    ).sort(
        "created_at",
        1
    )

    result = []

    for message in messages:

        result.append({
            "id": str(message["_id"]),
            "role": message["role"],
            "content": message["content"],
            "created_at": message["created_at"]
        })

    return result