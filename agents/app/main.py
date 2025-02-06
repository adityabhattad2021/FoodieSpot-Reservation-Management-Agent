from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    result = await agent.run(request.message)
    return ChatResponse(response=result.get("messages","There was an error processing your request"))
