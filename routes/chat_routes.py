from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user

from models.chat_model import CreateChatSession

from services.chat_service import (
    create_chat_session,
    get_user_chat_sessions
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