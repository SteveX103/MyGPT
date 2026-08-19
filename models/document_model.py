from pydantic import BaseModel
from datetime import datetime

class RenameDocument(BaseModel):
    filename: str

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    content_type: str
    uploaded_at: str