from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class ChatBase(BaseModel):
    user_id: int

class ChatResponse(BaseModel):
    id: UUID
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
    
class ChatCreate(ChatBase):
    title: str

class ChatUpdate(BaseModel):
    title: str