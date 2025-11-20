from pydantic import BaseModel, Field
from typing import Optional


class LookupRequest(BaseModel):
    """Request model for claim lookup"""
    phone: str = Field(..., description="Phone number associated with the claim")


class Claim(BaseModel):
    """Claim data model"""
    phone: str
    first_name: str
    last_name: str
    claim_status: str  # approved, pending, requires_documentation
    claim_id: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone": "5551234567",
                "first_name": "John",
                "last_name": "Doe",
                "claim_status": "approved",
                "claim_id": "CLM-2024-001",
                "email": "john.doe@example.com"
            }
        }
