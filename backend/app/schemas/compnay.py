from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class CompanyInfo(BaseModel):
    """Basic company information"""
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    employee_count: Optional[int] = None
    founded_year: Optional[int] = None
    headquarters: Optional[str] = None
    country: Optional[str] = None


class CompanyResearchRequest(BaseModel):
    """Schema for company research request"""
    company_name: str = Field(..., min_length=2)
    domain: Optional[str] = None


class CompanyResearchResponse(BaseModel):
    """Schema for company research response"""
    company_name: str
    company_domain: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    founded_year: Optional[int] = None
    funding_stage: Optional[str] = None
    total_funding: Optional[float] = None
    last_funding_date: Optional[str] = None
    executives: List[Dict[str, str]] = Field(default_factory=list)
    recent_news: List[Dict[str, Any]] = Field(default_factory=list)
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    tech_stack: List[str] = Field(default_factory=list)
    competitors: List[str] = Field(default_factory=list)
    trust_signals: List[str] = Field(default_factory=list)
    researched_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }