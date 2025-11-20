from fastapi import APIRouter, HTTPException
from app.models.claim import LookupRequest
from app.services.claim_service import ClaimRepository

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/lookup")
async def lookup_claim(request: LookupRequest):
    """
    Look up claim information by phone number
    
    - **phone**: Phone number associated with the claim
    
    Returns claim details if found, or {"found": False} if not found
    """
    claim_repo = ClaimRepository()
    result = await claim_repo.get_claim_by_phone(request.phone)
    
    if not result.get("found"):
        return {"found": False, "message": "No claim found for this phone number"}
    
    return result

