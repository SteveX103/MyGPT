from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user

from models.chat_model import CreateChatSession

from services.chat_service import (
    create_chat_session,
    get_user_chat_sessions
)

from models.chat_model import (
    CreateChatSession,
    CreateChatMessage,
    create_chat_message,
    get_chat_messages
)

router = APIRouter()


@router.post("/sessions")
def create_session(
    data: CreateChatSession,
    current_user=Depends(get_current_user)
):
    return create_chat_session(
        data,
        current_user
    )
@router.get("/sessions")
def get_sessions(
    current_user=Depends(get_current_user)
):
    return get_user_chat_sessions(
        current_user
    )
@router.post("/sessions/{session_id}/messages")
def send_message(
    session_id: str,
    data: CreateChatMessage,
    current_user=Depends(get_current_user)
):
    return create_chat_message(
        session_id=session_id,
        data=data,
        current_user=current_user,
        role="user"
    )
@router.get("/sessions/{session_id}/messages")
def get_messages(
    session_id: str,
    current_user=Depends(get_current_user)
):
    return get_chat_messages(
        session_id=session_id,
        current_user=current_user
    )