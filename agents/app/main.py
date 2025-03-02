from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .schemas import ChatRequest, ChatResponse, GetConversationHistoryResponse
from .session_manager import SessionManager
from .core.foodiespot_agent import FoodieSpotAgent
from .core.vector_store import init_vector_index
from .core.utils.api_client import APIClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_vector_index()
    yield
    # Currently nothing to do here (when the app is shutting down)

app = FastAPI(
    title="Restaurant Agent API",
    description="Chat API for restaurant management agent",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = FoodieSpotAgent()
session_manager = SessionManager(session_timeout=3600) 
api_client = APIClient()

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        session_id = str(request.session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    session_manager.add_message(session_id, "user", request.message)

    user_data = None
    if request.user_id:
        session = session_manager.get_session(session_id)
        if not hasattr(session,'user_data') or not session.user_data:
            user_data = await api_client.get_user_details(request.user_id)
            if "error" not in user_data:
                session.user_data = user_data
    
    result = await agent.run(request.message,session.user_data)
    response = result["message"]
    
    session_manager.add_message(session_id, "assistant", response)
    return ChatResponse(response=str(response), session_id=session_id)

@app.get("/conversation/{session_id}", response_model=GetConversationHistoryResponse, tags=["Chat"])
async def get_conversation_history(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        agent.clear()
        session = session_manager.create_session()
    
    return GetConversationHistoryResponse(
        history=session.messages,
        session_id=session.id
    )

@app.delete("/session/{session_id}", tags=["Chat"])
async def clear_session(session_id: str):
    session_manager.delete_session(session_id)
    return {"message": "Session cleared"}