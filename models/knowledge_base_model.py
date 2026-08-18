from pydantic import BaseModel
from typing import Optional


class CreateKnowledgeBase(BaseModel):
    name: str
    description: Optional[str] = None

class UpdateKnowledgeBase(BaseModel):
    name: str | None = None
    description: str | None = None