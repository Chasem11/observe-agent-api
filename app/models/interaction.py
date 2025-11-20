from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class InteractionLog(BaseModel):
    """Model for logging customer interactions"""
    caller_name: Optional[str] = Field(None, description="Full name of the caller")
    phone: Optional[str] = Field(None, description="Caller's phone number")
    summary: str = Field(..., description="Summary of the conversation")
    sentiment: str = Field(..., description="Sentiment analysis: positive, neutral, or negative")
    timestamp: Optional[str] = Field(None, description="ISO timestamp of the interaction")
    call_duration: Optional[int] = Field(None, description="Duration of call in seconds")
    topics: Optional[List[str]] = Field(default_factory=list, description="Topics discussed during call")
    
    class Config:
        json_schema_extra = {
            "example": {
                "caller_name": "John Doe",
                "phone": "5551234567",
                "summary": "Customer called to check claim status. Claim was approved. Customer satisfied.",
                "sentiment": "positive",
                "timestamp": "2025-11-19T10:30:00Z",
                "call_duration": 120,
                "topics": ["claim_status", "authentication"]
            }
        }
