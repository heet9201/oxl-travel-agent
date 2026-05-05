from fastapi import APIRouter, HTTPException
from models.schemas import ChatRequest, ChatResponse
from agents.orchestrator import OrchestratorAgent
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])
orchestrator = OrchestratorAgent()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - processes user messages through the orchestrator."""
    try:
        history = [msg.model_dump() for msg in request.conversation_history] if request.conversation_history else []
        result = await orchestrator.process_message(
            message=request.message,
            conversation_history=history,
            trip_context=request.trip_context,
        )
        return ChatResponse(
            reply=result.get("reply", "We’re having trouble processing your request right now. Please try again."),
            message_type=result.get("message_type", "text"),
            data=result.get("data"),
            trip_context=result.get("trip_context"),
        )
    except Exception as e:
        logger.error(f"Internal Error in chat endpoint: {str(e)}")
        # Return generic error response instead of HTTP 500 so UI doesn't crash
        return ChatResponse(
            reply="We’re having trouble processing your request right now. Please try again.",
            message_type="text",
            data=None,
            trip_context=request.trip_context,
        )
