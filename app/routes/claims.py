from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.services.claim_service import ClaimRepository
from app.core.vapi_serializer import get_normalized_body, format_vapi_response
from app.core.logger import get_logger

logger = get_logger("claims-route")

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/lookup")
async def lookup_claim(request: Request):
    """
    Look up claim information by phone number
    
    VAPI Tool Call Endpoint
    """
    try:
        # Get normalized body from middleware
        body = await get_normalized_body(request)
        logger.info(f"Processing claim lookup - body: {body}")
        
        phone = body.get("phone")
        
        if not phone:
            logger.warning("Phone number missing from request")
            error_result = {"error": "Phone is required", "found": False}
            return JSONResponse(
                format_vapi_response(request, error_result),
                status_code=400
            )
        
        # Use the repository to lookup claim
        claim_repo = ClaimRepository()
        result = await claim_repo.get_claim_by_phone(str(phone))
        
        if not result.get("found"):
            logger.info(f"Claim not found for phone: {phone}")
            result = {"found": False, "message": "No claim found for this phone number"}
        else:
            logger.info(f"Claim found for phone: {phone}")
        
        # Format response for VAPI (or return directly if not VAPI)
        return JSONResponse(format_vapi_response(request, result))
        
    except Exception as err:
        logger.error(f"Error in lookup_claim: {err}", exc_info=True)
        error_result = {"error": "Internal server error", "found": False}
        return JSONResponse(
            format_vapi_response(request, error_result),
            status_code=500
        )

