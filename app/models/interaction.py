from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class InteractionLog(BaseModel):
    """Model for logging customer interactions at end of call"""
    caller_name: Optional[str] = Field(None, description="Full name of the caller (if authenticated)")
    phone: Optional[str] = Field(None, description="Caller's phone number")
    summary: str = Field(..., description="Summary of the conversation")
    sentiment: str = Field(..., description="Call sentiment: positive, neutral, or negative")
    timestamp: Optional[str] = Field(None, description="ISO timestamp of the interaction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "caller_name": "John Doe",
                "phone": "5551234567",
                "summary": "Customer called to check claim status. Claim was approved. Customer confirmed identity and was satisfied with the information.",
                "sentiment": "positive",
                "timestamp": "2025-11-20T10:30:00Z"
            }
        }
