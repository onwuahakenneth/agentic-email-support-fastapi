from typing import Optional
from typing import TypedDict
from datetime import datetime
from dataclasses import dataclass
from pydantic import BaseModel, Field



# Chat Message
class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    email_content: str
    email_sender: str


class ChatResponse(BaseModel):
    id: str
    role: str = "assistant"
    content: str
    timestamp: datetime