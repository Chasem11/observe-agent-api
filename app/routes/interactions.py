from fastapi import APIRouter, Request
from typing import Optional
from app.models.interaction import InteractionLog
from app.services.interaction_service import InteractionRepository
from app.core.vapi_serializer import get_normalized_body, format_vapi_response

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("/log")
async def log_interaction(request: Request):
    """
    Log a customer interaction after a call
    
    VAPI Tool Call Endpoint
    
    Records call summary, sentiment, and metadata for analytics
    
    Expects VAPI format with interaction data in arguments
    """
    try:
        # Get normalized body from middleware
        body = await get_normalized_body(request)
        
        # Validate with Pydantic model
        interaction = InteractionLog(**body)
        
        interaction_repo = InteractionRepository()
        result = await interaction_repo.log_interaction(interaction)
        
        # Return in VAPI format
        return format_vapi_response(request, result)
        
    except Exception as e:
        print(f"Error logging interaction: {e}")
        error_result = {"success": False, "error": str(e)}
        return format_vapi_response(request, error_result)

