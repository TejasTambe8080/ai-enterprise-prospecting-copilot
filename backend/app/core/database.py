from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

from app.config.settings import settings

logger = logging.getLogger(__name__)

class MongoDB:
    """MongoDB connection manager with singleton pattern"""
    
    _instance = None
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    async def connect(cls):
        """Establish connection to MongoDB"""
        try:
            if cls.client is None:
                cls.client = AsyncIOMotorClient(
                    settings.MONGODB_URI,
                    maxPoolSize=50,
                    minPoolSize=10,
                    maxIdleTimeMS=60000,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000
                )
                cls.db = cls.client[settings.MONGODB_DB_NAME]
                
                # Test connection
                await cls.client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
                
                # Create indexes
                await cls.create_indexes()
                
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            logger.info("MongoDB connection closed")
    
    @classmethod
    async def create_indexes(cls):
        """Create necessary indexes for performance"""
        try:
            # Leads collection indexes
            await cls.db.leads.create_index([("email", 1)], unique=True)
            await cls.db.leads.create_index([("company_name", 1)])
            await cls.db.leads.create_index([("status", 1)])
            await cls.db.leads.create_index([("created_at", -1)])
            await cls.db.leads.create_index([("tenant_id", 1), ("status", 1)])
            await cls.db.leads.create_index([("meddpicc_score.total_score", -1)])
            await cls.db.leads.create_index([("created_at", -1), ("status", 1)])
            
            # Companies collection indexes
            await cls.db.companies.create_index([("name", 1)], unique=True)
            await cls.db.companies.create_index([("domain", 1)], unique=True)
            await cls.db.companies.create_index([("industry", 1)])
            await cls.db.companies.create_index([("employee_count", -1)])
            
            # Case studies collection indexes
            await cls.db.case_studies.create_index([("title", 1)])
            await cls.db.case_studies.create_index([("industry", 1)])
            await cls.db.case_studies.create_index([("category", 1)])
            
            # Agent logs collection indexes
            await cls.db.agent_logs.create_index([("lead_id", 1)])
            await cls.db.agent_logs.create_index([("agent_name", 1)])
            await cls.db.agent_logs.create_index([("created_at", -1)])
            
            # Embeddings collection indexes (for vector search)
            await cls.db.embeddings.create_index([("vector", "2dsphere")])
            
            logger.info("Database indexes created")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
            raise
    
    @classmethod
    async def get_collection(cls, collection_name: str):
        """Get collection by name"""
        if cls.db is None:
            await cls.connect()
        return cls.db[collection_name]

# Helper functions
async def get_database() -> AsyncIOMotorDatabase:
    """Get database instance for dependency injection"""
    if MongoDB.db is None:
        await MongoDB.connect()
    return MongoDB.db

async def connect_to_mongo():
    """Connect to MongoDB"""
    await MongoDB.connect()

async def close_mongo_connection():
    """Close MongoDB connection"""
    await MongoDB.close()

# Repository class for common operations
class BaseRepository:
    """Base repository with common CRUD operations"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self._collection = None
    
    async def get_collection(self):
        if self._collection is None:
            self._collection = await MongoDB.get_collection(self.collection_name)
        return self._collection
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        collection = await self.get_collection()
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        result = await collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data
    
    async def find_one(self, filter: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        collection = await self.get_collection()
        result = await collection.find_one(filter)
        if result:
            result["_id"] = str(result["_id"])
        return result
    
    async def find_many(self, filter: Dict[str, Any], limit: int = 100, skip: int = 0, sort: List = None) -> List[Dict[str, Any]]:
        collection = await self.get_collection()
        cursor = collection.find(filter)
        if sort:
            cursor = cursor.sort(sort)
        cursor = cursor.skip(skip).limit(limit)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results
    
    async def update(self, filter: Dict[str, Any], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        collection = await self.get_collection()
        data["updated_at"] = datetime.utcnow()
        result = await collection.update_one(filter, {"$set": data})
        if result.modified_count > 0:
            return await self.find_one(filter)
        return None
    
    async def delete(self, filter: Dict[str, Any]) -> bool:
        collection = await self.get_collection()
        result = await collection.delete_one(filter)
        return result.deleted_count > 0