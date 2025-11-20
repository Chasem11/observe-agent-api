import os
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FirestoreClient:
    """Singleton Firestore client"""
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreClient, cls).__new__(cls)
            cls._initialize_client()
        return cls._instance
    
    @classmethod
    def _initialize_client(cls):
        """Initialize Firestore client with credentials"""
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path:
            cls._db = firestore.Client.from_service_account_json(credentials_path)
        else:
            # Fallback to default credentials (useful for deployed environments)
            cls._db = firestore.Client()
    
    @classmethod
    def get_db(cls) -> firestore.Client:
        """Get Firestore database instance"""
        if cls._db is None:
            cls._initialize_client()
        return cls._db


def get_firestore_db() -> firestore.Client:
    """Dependency injection for Firestore client"""
    return FirestoreClient.get_db()
