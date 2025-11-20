from google.cloud import firestore
from datetime import datetime
from typing import Optional, List, Dict
from app.models.interaction import InteractionLog
from app.core.database import get_firestore_db


class InteractionRepository:
    """Repository for interaction logging operations"""
    
    def __init__(self, db: firestore.Client = None):
        self.db = db or get_firestore_db()
        self.collection = "interactions"
    
    async def log_interaction(self, interaction: InteractionLog) -> Dict:
        """
        Log a customer interaction
        
        Args:
            interaction: InteractionLog model with call details
            
        Returns:
            Success status and document ID
        """
        try:
            # Add timestamp if not provided
            interaction_data = interaction.model_dump()
            if not interaction_data.get("timestamp"):
                interaction_data["timestamp"] = datetime.utcnow().isoformat()
            
            # Create document in Firestore
            doc_ref = self.db.collection(self.collection).document()
            doc_ref.set(interaction_data)
            
            return {
                "success": True,
                "message": "Interaction logged successfully",
                "id": doc_ref.id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    