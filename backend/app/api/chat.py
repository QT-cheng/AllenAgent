from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from backend.app.agents.graph import app_agent
from backend.app.agents.state import AgentState
from backend.app.db.session import get_chat_history, save_chat_message
from langchain_core.messages import HumanMessage, AIMessage


class ChatRequest(BaseModel):
    session_id: str
    query: str


class ChatResponse(BaseModel):
    answer: str


router = APIRouter(prefix="/chat")


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        history_msgs = get_chat_history(session_id)
        state: AgentState = {
            "messages": history_msgs,
            "original_query": request.query,
            "rewritten_query": "",
            "retrieved_docs": [],
            "draft_answer": "",
            "final_answer": "",
            "needs_correction": False,
            "count_generate": 0
        }
        result = app_agent.invoke(state)
        save_chat_message(session_id, HumanMessage(content=request.query))
        save_chat_message(session_id, AIMessage(content=result["final_answer"]))
        return ChatResponse(answer=result["final_answer"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
