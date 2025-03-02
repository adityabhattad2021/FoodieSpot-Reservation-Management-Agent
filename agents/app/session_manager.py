import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, List
from .schemas import Message, User

class Session:
    def __init__(self,id:str,messages):
        self.id = id
        self.messages: List[Message] = messages
        self.last_activity: datetime = datetime.now(timezone.utc)
        self.user_data: Optional[User] = None

    def set_user_data(self, user_data: User):
        self.user_data = user_data
        self.last_activity = datetime.now(timezone.utc)

    def add_message(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))
        self.last_activity =  datetime.now(timezone.utc)

class SessionManager:
    def __init__(self, session_timeout: int = 3600):
        self._sessions: Dict[str, Session] = {}
        self.session_timeout = session_timeout
        
    def _cleanup_expired_sessions(self) -> None:
        current_time = datetime.now(timezone.utc)  
        expired_sessions = [
            session_id
            for session_id, session in self._sessions.items()
            if (current_time - session.last_activity).total_seconds() > self.session_timeout
        ]
        for session_id in expired_sessions:
            del self._sessions[session_id]

    def get_session(self, session_id: str) -> Optional[Session]:
        self._cleanup_expired_sessions()
        session = self._sessions.get(session_id)
        if session:
            session.last_activity = datetime.now(timezone.utc)  
        return session

    def create_session(self) -> Session:
        session = Session(
            id=str(uuid.uuid4()),
            messages=[
                Message(
                    role="assistant",
                    content="*Hello!* I'm your **FoodieSpot** assistant. How can I help you today?"
                )
            ]
        )
        self._sessions[session.id] = session
        return session

    def add_message(self, session_id: str, role: str, content: str) -> None:
        session = self.get_session(session_id)
        if not session:
            session = self.create_session()
            self._sessions[session_id] = session
        session.add_message(role, content)
        return session.id 

    def delete_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)