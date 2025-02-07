from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ChatRequest, ChatResponse, GetConversationHistoryResponse
from .session_manager import SessionManager
from .core.router import RouterAgent

app = FastAPI(
    title="Restaurant Agent API",
    description="Chat API for restaurant management agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = RouterAgent()
session_manager = SessionManager(session_timeout=3600) 

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        session_id = str(request.session_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    session_manager.add_message(session_id, "user", request.message)
    
    result = await agent.run(request.message)
    response = result.get("messages", "There was an error processing your request")
    
    session_manager.add_message(session_id, "assistant", response)
    return ChatResponse(response=response, session_id=session_id)

@app.get("/conversation/{session_id}", response_model=GetConversationHistoryResponse, tags=["Chat"])
async def get_conversation_history(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        session = session_manager.create_session()
    
    return GetConversationHistoryResponse(
        history=session.messages,
        session_id=session_id
    )

@app.delete("/session/{session_id}", tags=["Chat"])
async def clear_session(session_id: str):
    session_manager.delete_session(session_id)
    new_session = session_manager.create_session()
    return {"message": "Session cleared", "session_id": new_session.id}