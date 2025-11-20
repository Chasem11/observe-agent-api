from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.claim_service import ClaimRepository
import json

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/lookup")
async def lookup_claim(request: Request):
    """
    Look up claim information by phone number
    
    Expects VAPI format with arguments field
    
    Returns claim details if found, or {"found": False} if not found
    """
    try:
        body = await request.json()
        
        # Parse VAPI-style arguments
        if "arguments" not in body:
            return JSONResponse(
                {"error": "Missing arguments field", "found": False}, 
                status_code=400
            )
        
        args = body["arguments"]
        
        # VAPI sends arguments as a string — parse it into JSON
        if isinstance(args, str):
            args = json.loads(args)
        
        phone = args.get("phone")
        
        if not phone:
            return JSONResponse(
                {"error": "Phone is required", "found": False}, 
                status_code=400
            )
        
        # Use the repository to lookup claim
        claim_repo = ClaimRepository()
        result = await claim_repo.get_claim_by_phone(str(phone))
        
        if not result.get("found"):
            return JSONResponse({"found": False, "message": "No claim found for this phone number"})
        
        return JSONResponse(result)
        
    except json.JSONDecodeError:
        return JSONResponse(
            {"error": "Invalid JSON in arguments", "found": False}, 
            status_code=400
        )
    except Exception as err:
        print(f"Error in lookup_claim: {err}")
        return JSONResponse(
            {"error": "Internal server error", "found": False}, 
            status_code=500
        )

