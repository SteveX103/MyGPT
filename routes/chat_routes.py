from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user

from models.chat_model import CreateChatSession

from services.chat_service import (
    create_chat_session
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