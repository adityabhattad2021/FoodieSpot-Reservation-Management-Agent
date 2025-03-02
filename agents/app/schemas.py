from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone


class IntentClassificationResponse(BaseModel):
    category: str

class ReservationDetailsExtractorResponse(BaseModel):
    restaurant_name: str
    date: str
    time: str
    party_size: int
    has_user_confirmed: bool


class Reservation(BaseModel):
    restaurant_id: int
    reservation_date: datetime
    reservation_time: datetime
    number_of_guests: int
    reservation_id: int
    user_id: int
    status: str
    reservation_code: str

class User(BaseModel):
    name: str
    email: str
    user_id: int
    ai_preferences: Optional[str] = None

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
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class GetConversationHistoryResponse(BaseModel):
    history: List[Message]
    session_id: str