from fastapi import APIRouter, Query
from typing import Optional
from app.models.interaction import InteractionLog
from app.services.interaction_service import InteractionRepository

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("/log")
async def log_interaction(interaction: InteractionLog):
    """
    Log a customer interaction after a call
    
    Records call summary, sentiment, and metadata for analytics
    """
    interaction_repo = InteractionRepository()
    result = await interaction_repo.log_interaction(interaction)
    
    return result

