from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now(timezone.utc)

class Session(BaseModel):
    id: str
    messages: List[Message] = []
    created_at: datetime = datetime.now(timezone.utc)
    last_activity: datetime = datetime.now(timezone.utc)

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    session_id: str

class GetConversationHistoryResponse(BaseModel):
    history: List[Message]
    session_id: str