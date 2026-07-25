from typing import Dict, Any, Optional, List
from datetime import datetime
from bson import ObjectId

from app.core.database import MongoDB
from app.models.lead import Lead, LeadStatus
from app.utils.validators import validate_lead_data
from app.core.logging import get_logger

logger = get_logger(__name__)

class LeadService:
    """Service for lead management operations"""
    
    def __init__(self):
        self.collection_name = "leads"
        self.logger = logger
    
    async def get_collection(self):
        """Get leads collection"""
        return await MongoDB.get_collection(self.collection_name)
    
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead"""
        try:
            # Validate lead data
            errors = validate_lead_data(lead_data)
            if errors:
                return {
                    "status": "error",
                    "errors": errors,
                    "message": "Validation failed"
                }
            
            collection = await self.get_collection()
            
            # Check for duplicate
            existing = await collection.find_one({"email": lead_data.get("email")})
            if existing:
                return {
                    "status": "error",
                    "message": "Lead with this email already exists",
                    "lead_id": str(existing["_id"])
                }
            
            # Prepare lead document
            lead_doc = {
                **lead_data,
                "status": LeadStatus.PENDING,
                "processing_stage": "received",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "agent_logs": [],
                "pain_points": [],
                "opportunities": [],
                "personalized_emails": [],
                "decision_makers": []
            }
            
            # Insert lead
            result = await collection.insert_one(lead_doc)
            lead_id = str(result.inserted_id)
            
            self.logger.info(f"Lead created successfully: {lead_id}")
            
            return {
                "status": "success",
                "message": "Lead created successfully",
                "lead_id": lead_id
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create lead: {str(e)}")
            raise
    
    async def get_lead_by_id(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get lead by ID"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(lead_id):
                return None
            
            result = await collection.find_one({"_id": ObjectId(lead_id)})
            
            if result:
                result["id"] = str(result["_id"])
                del result["_id"]
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get lead: {str(e)}")
            return None
    
    async def get_leads(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get leads with pagination and filtering"""
        try:
            collection = await self.get_collection()
            
            # Build filter
            filter_query = {}
            if status:
                filter_query["status"] = status
            if search:
                filter_query["$or"] = [
                    {"first_name": {"$regex": search, "$options": "i"}},
                    {"last_name": {"$regex": search, "$options": "i"}},
                    {"company_name": {"$regex": search, "$options": "i"}},
                    {"email": {"$regex": search, "$options": "i"}}
                ]
            
            # Get total count
            total = await collection.count_documents(filter_query)
            
            # Get leads
            cursor = collection.find(filter_query).sort("created_at", -1).skip(skip).limit(limit)
            leads = []
            async for doc in cursor:
                doc["id"] = str(doc["_id"])
                del doc["_id"]
                leads.append(doc)
            
            return {
                "data": leads,
                "pagination": {
                    "total": total,
                    "skip": skip,
                    "limit": limit,
                    "pages": (total + limit - 1) // limit if total > 0 else 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get leads: {str(e)}")
            raise
    
    async def update_lead(self, lead_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a lead"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(lead_id):
                return None
            
            update_data["updated_at"] = datetime.utcnow()
            
            result = await collection.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return await self.get_lead_by_id(lead_id)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to update lead: {str(e)}")
            raise
    
    async def update_lead_status(self, lead_id: str, status: LeadStatus, error_message: Optional[str] = None) -> bool:
        """Update lead status"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(lead_id):
                return False
            
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow()
            }
            
            if status == LeadStatus.QUALIFIED:
                update_data["qualified_at"] = datetime.utcnow()
            
            if status == LeadStatus.PROCESSING:
                update_data["processing_stage"] = "processing"
            
            if status == LeadStatus.ERROR and error_message:
                update_data["error_message"] = error_message
            
            result = await collection.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            self.logger.error(f"Failed to update lead status: {str(e)}")
            return False
    
    async def add_agent_log(self, lead_id: str, agent_name: str, log_data: Dict[str, Any]) -> bool:
        """Add agent execution log to lead"""
        try:
            collection = await self.get_collection()
            
            if not ObjectId.is_valid(lead_id):
                return False
            
            log_entry = {
                "agent_name": agent_name,
                "timestamp": datetime.utcnow(),
                **log_data
            }
            
            result = await collection.update_one(
                {"_id": ObjectId(lead_id)},
                {"$push": {"agent_logs": log_entry}}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            self.logger.error(f"Failed to add agent log: {str(e)}")
            return False
    
    async def get_lead_stats(self) -> Dict[str, Any]:
        """Get lead statistics"""
        try:
            collection = await self.get_collection()
            
            total = await collection.count_documents({})
            qualified = await collection.count_documents({"status": LeadStatus.QUALIFIED})
            processing = await collection.count_documents({"status": LeadStatus.PROCESSING})
            pending = await collection.count_documents({"status": LeadStatus.PENDING})
            disqualified = await collection.count_documents({"status": LeadStatus.DISQUALIFIED})
            
            # Get average score
            pipeline = [
                {"$match": {"meddpicc_score.total_score": {"$exists": True}}},
                {"$group": {
                    "_id": None,
                    "avg_score": {"$avg": "$meddpicc_score.total_score"}
                }}
            ]
            cursor = collection.aggregate(pipeline)
            avg_result = await cursor.to_list(length=1)
            avg_score = avg_result[0]["avg_score"] if avg_result else 0
            
            return {
                "total": total,
                "qualified": qualified,
                "processing": processing,
                "pending": pending,
                "disqualified": disqualified,
                "avg_score": round(avg_score, 1) if avg_score else 0,
                "conversion_rate": round((qualified / total * 100), 1) if total > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get lead stats: {str(e)}")
            return {}