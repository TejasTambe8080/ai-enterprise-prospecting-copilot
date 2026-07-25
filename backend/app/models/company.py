from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class Company(BaseModel):
    """Company model"""
    id: Optional[str] = None
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    
    # Company details
    employee_count: Optional[int] = None
    revenue: Optional[str] = None
    funding_stage: Optional[str] = None
    total_funding: Optional[float] = None
    founded_year: Optional[int] = None
    
    # Location
    headquarters: Optional[str] = None
    country: Optional[str] = None
    
    # Technology
    technologies: List[str] = Field(default_factory=list)
    social_links: Dict[str, str] = Field(default_factory=dict)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_researched: Optional[datetime] = None

class CompanyResearch(BaseModel):
    """Company research results"""
    company_name: str
    company_domain: str
    
    # Basic info
    description: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    founded_year: Optional[int] = None
    
    # Financial info
    funding_stage: Optional[str] = None
    total_funding: Optional[float] = None
    last_funding_date: Optional[str] = None
    
    # Leadership
    executives: List[Dict[str, str]] = Field(default_factory=list)
    
    # News
    recent_news: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Social presence
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    
    # Technology stack
    tech_stack: List[str] = Field(default_factory=list)
    
    # Competitors
    competitors: List[str] = Field(default_factory=list)
    
    # Trust signals
    trust_signals: List[str] = Field(default_factory=list)
    
    # Timestamp
    researched_at: datetime = Field(default_factory=datetime.utcnow)