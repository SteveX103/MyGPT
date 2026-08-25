from pydantic import BaseModel


class CreateChatSession(BaseModel):
    title: str = "New Chat"
    knowledge_base_id: str


class UpdateChatSession(BaseModel):
    title: str