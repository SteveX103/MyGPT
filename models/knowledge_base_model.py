from pydantic import BaseModel
from typing import Optional


class CreateKnowledgeBase(BaseModel):
    name: str
    description: Optional[str] = None