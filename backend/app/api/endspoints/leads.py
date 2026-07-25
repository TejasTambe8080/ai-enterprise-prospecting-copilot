from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio

from app.models.lead import Lead, LeadStatus
from pydantic import BaseModel, Field
from app.core.database import MongoDB, get_database
from app.agents.orchestrator import AgentOrchestrator
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


class EmailProcessingRequest(BaseModel):
    email_content: str = Field(min_length=1, max_length=100_000)

@router.post("/")
async def create_lead(lead: Lead) -> Dict[str, Any]:
    """Create a new lead"""
    try:
        db = await get_database()
        collection = db["leads"]
        
        # Check if lead already exists
        existing = await collection.find_one({"email": lead.email})
        if existing:
            raise HTTPException(status_code=409, detail="Lead with this email already exists")
        
        # Insert lead
        result = await collection.insert_one(lead.dict(by_alias=True))
        
        return {
            "status": "success",
            "message": "Lead created successfully",
            "lead_id": str(result.inserted_id)
        }
    except Exception as e:
        logger.error(f"Failed to create lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[LeadStatus] = None,
    search: Optional[str] = None
) -> Dict[str, Any]:
    """Get leads with pagination and filtering"""
    try:
        db = await get_database()
        collection = db["leads"]
        
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
            "status": "success",
            "data": leads,
            "pagination": {
                "total": total,
                "skip": skip,
                "limit": limit,
                "pages": (total + limit - 1) // limit
            }
        }
    except Exception as e:
        logger.error(f"Failed to fetch leads: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{lead_id}")
async def get_lead(lead_id: str) -> Dict[str, Any]:
    """Get lead by ID"""
    try:
        db = await get_database()
        collection = db["leads"]
        
        from bson import ObjectId
        doc = await collection.find_one({"_id": ObjectId(lead_id)})
        
        if not doc:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        
        return {
            "status": "success",
            "data": doc
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{lead_id}/process")
async def process_lead(lead_id: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Process a lead through the agent pipeline"""
    try:
        db = await get_database()
        collection = db["leads"]
        
        from bson import ObjectId
        lead = await collection.find_one({"_id": ObjectId(lead_id)})
        
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        
        # Update status to processing
        await collection.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": {"status": LeadStatus.PROCESSING, "updated_at": datetime.utcnow()}}
        )
        
        # Process in background
        background_tasks.add_task(
            _process_lead_background,
            lead_id,
            lead.get("message", ""),
            lead.get("email", "")
        )
        
        return {
            "status": "success",
            "message": "Lead processing started",
            "lead_id": lead_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to process lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-email")
async def process_email(payload: EmailProcessingRequest) -> Dict[str, Any]:
    """Process an email directly"""
    try:
        # Create orchestrator
        orchestrator = AgentOrchestrator()
        
        # Process lead
        result = await orchestrator.process_lead(payload.email_content)
        
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        logger.error(f"Failed to process email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def _process_lead_background(lead_id: str, message: str, email: str):
    """Background task for lead processing"""
    try:
        db = await get_database()
        collection = db["leads"]
        
        from bson import ObjectId
        
        # Get lead
        lead = await collection.find_one({"_id": ObjectId(lead_id)})
        if not lead:
            logger.error(f"Lead {lead_id} not found")
            return
        
        # Create orchestrator
        orchestrator = AgentOrchestrator()
        
        # Process lead
        result = await orchestrator.process_lead(
            message or f"Lead from {lead.get('first_name', '')} {lead.get('last_name', '')} at {lead.get('company_name', '')}",
            lead_id
        )
        
        logger.info(f"Lead {lead_id} processed successfully")
        
    except Exception as e:
        logger.error(f"Background processing failed for lead {lead_id}: {str(e)}")
        # Update status to error
        try:
            from bson import ObjectId
            await collection.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": {"status": LeadStatus.ERROR, "error_message": str(e)}}
            )
        except:
            pass
