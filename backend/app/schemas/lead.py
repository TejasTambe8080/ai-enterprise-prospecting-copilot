from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum

from app.models.lead import LeadStatus, GTM_Motion, MEDDPICCScore


class LeadCreate(BaseModel):
    """Schema for creating a new lead"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company_name: str = Field(..., min_length=2, max_length=200)
    company_domain: Optional[str] = None
    message: Optional[str] = None
    source: str = Field(default="website_form")
    source_details: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('phone')
    def validate_phone(cls, v):
        if v:
            # Remove formatting characters
            cleaned = ''.join(filter(str.isdigit, v))
            if len(cleaned) < 10:
                raise ValueError('Phone number must have at least 10 digits')
        return v


class LeadUpdate(BaseModel):
    """Schema for updating a lead"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = Field(None, min_length=2, max_length=200)
    company_domain: Optional[str] = None
    status: Optional[LeadStatus] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    funding_stage: Optional[str] = None
    pain_points: Optional[List[str]] = None
    opportunities: Optional[List[str]] = None


class LeadResponse(BaseModel):
    """Schema for lead response"""
    id: str
    tenant_id: str = "default"
    
    # Contact Information
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company_name: str
    company_domain: Optional[str] = None
    
    # Source Information
    source: str
    source_details: Dict[str, Any]
    message: Optional[str] = None
    intent: Optional[str] = None
    urgency: Optional[str] = None
    
    # Processing Status
    status: LeadStatus
    processing_stage: str
    error_message: Optional[str] = None
    
    # Company Intelligence
    company_data: Dict[str, Any]
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    funding_stage: Optional[str] = None
    revenue_range: Optional[str] = None
    
    # MEDDPICC Scoring
    meddpicc_score: Optional[MEDDPICCScore] = None
    
    # Pain Points
    pain_points: List[str]
    opportunities: List[str]
    
    # Outreach Content
    personalized_emails: List[Dict[str, str]]
    linkedin_message: Optional[str] = None
    
    # GTM Motion
    recommended_motion: Optional[GTM_Motion] = None
    motion_reasoning: Optional[str] = None
    
    # Case Study
    matched_case_study: Optional[Dict[str, Any]] = None
    
    # Decision Makers
    decision_makers: List[Dict[str, Any]]
    
    # Agent Logs
    agent_logs: List[Dict[str, Any]]
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime] = None
    qualified_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True


class LeadListResponse(BaseModel):
    """Schema for paginated lead list response"""
    data: List[LeadResponse]
    pagination: Dict[str, Any]


class LeadProcessRequest(BaseModel):
    """Schema for lead processing request"""
    email_content: str = Field(..., min_length=1)
    lead_id: Optional[str] = None


class LeadProcessResponse(BaseModel):
    """Schema for lead processing response"""
    status: str
    message: str
    lead_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    agent_status: Optional[Dict[str, str]] = None