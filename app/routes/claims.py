from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.claim_service import ClaimRepository
from app.core.vapi_serializer import get_normalized_body, format_vapi_response

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/lookup")
async def lookup_claim(request: Request):
    """
    Look up claim information by phone number
    
    VAPI Tool Call Endpoint
    
    Expects VAPI format:
    {
      "attributes": {
        "id": "toolCallId",
        "function": {
          "name": "lookupClaim",
          "arguments": "{\"phone\":\"5551234567\"}"
        }
      }
    }
    
    Returns VAPI format:
    {
      "results": [{
        "toolCallId": "toolCallId",
        "result": { claim data or error }
      }]
    }
    """
    try:
        # Get normalized body from middleware
        body = await get_normalized_body(request)
        
        phone = body.get("phone")
        
        if not phone:
            error_result = {"error": "Phone is required", "found": False}
            return JSONResponse(
                format_vapi_response(request, error_result),
                status_code=400
            )
        
        # Use the repository to lookup claim
        claim_repo = ClaimRepository()
        result = await claim_repo.get_claim_by_phone(str(phone))
        
        if not result.get("found"):
            result = {"found": False, "message": "No claim found for this phone number"}
        
        # Format response for VAPI (or return directly if not VAPI)
        return JSONResponse(format_vapi_response(request, result))
        
    except Exception as err:
        print(f"Error in lookup_claim: {err}")
        error_result = {"error": "Internal server error", "found": False}
        return JSONResponse(
            format_vapi_response(request, error_result),
            status_code=500
        )

