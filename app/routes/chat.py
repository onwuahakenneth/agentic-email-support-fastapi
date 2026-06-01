import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from src.app.models import ChatResponse, ChatRequest
from src.app.services.email_support_service import email_support_service


router = APIRouter(prefix='/chat', tags=['chat'])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """send a message and get a response"""

    try:
        response_text = await email_support_service.process_chat(request)

        return ChatResponse(
            id=str(uuid.uuid4()),
            content=response_text,
            timestamp=datetime.now(timezone.utc),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health")
async def health_check(): 
    """health check endpoint"""
    
    return {"status": "OK"}