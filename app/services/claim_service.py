from google.cloud import firestore
from typing import Optional, Dict
from app.models.claim import Claim
from app.core.database import get_firestore_db


class ClaimRepository:
    """Repository for claim data operations"""
    
    def __init__(self, db: firestore.Client = None):
        self.db = db or get_firestore_db()
        self.collection = "claims"
    
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """Normalize phone number to digits only"""
        return "".join(filter(str.isdigit, phone))
    
    async def get_claim_by_phone(self, phone: str) -> Optional[Dict]:
        """
        Retrieve claim by phone number
        
        Args:
            phone: Phone number to lookup
            
        Returns:
            Claim data if found, None otherwise
        """
        normalized_phone = self.normalize_phone(phone)
        
        # Try direct document lookup (if phone is the document ID)
        doc_ref = self.db.collection(self.collection).document(normalized_phone)
        doc = doc_ref.get()
        
        if doc.exists:
            return {"found": True, **doc.to_dict()}
        
        # Fallback: Query by phone field
        results = (
            self.db.collection(self.collection)
            .where("phone", "==", normalized_phone)
            .limit(1)
            .stream()
        )
        
        for result in results:
            return {"found": True, **result.to_dict()}
        
        return {"found": False}
    
