from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum

class LeadStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"
    ERROR = "error"

class GTM_Motion(str, Enum):
    DIRECT_AE = "direct_ae"
    PARTNER_LED = "partner_led"
    SDR_LED = "sdr_led"

class MEDDPICCScore(BaseModel):
    """MEDDPICC framework scoring"""
    metrics: int = Field(ge=0, le=100, description="Measurable business impact")
    economic_buyer: int = Field(ge=0, le=100, description="Access to decision maker")
    decision_criteria: int = Field(ge=0, le=100, description="Solution alignment")
    decision_process: int = Field(ge=0, le=100, description="Purchase timeline clarity")
    paper_process: int = Field(ge=0, le=100, description="Procurement ease")
    internal_champion: int = Field(ge=0, le=100, description="Advocate existence")
    competition: int = Field(ge=0, le=100, description="Competitive position")
    
    @property
    def total_score(self) -> float:
        """Calculate weighted total score"""
        weights = {
            'metrics': 0.20,
            'economic_buyer': 0.15,
            'decision_criteria': 0.15,
            'decision_process': 0.15,
            'paper_process': 0.10,
            'internal_champion': 0.15,
            'competition': 0.10
        }
        
        score = sum(
            getattr(self, field) * weights[field]
            for field in weights
        )
        return round(score, 1)
    
    @property
    def qualification(self) -> str:
        """Get qualification level"""
        score = self.total_score
        if score >= 70:
            return "highly_qualified"
        elif score >= 50:
            return "qualified"
        elif score >= 30:
            return "needs_review"
        else:
            return "disqualified"

class Lead(BaseModel):
    """Main lead model"""
    id: Optional[str] = None
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
    source: str = "website_form"
    source_details: Dict[str, Any] = Field(default_factory=dict)
    message: Optional[str] = None
    intent: Optional[str] = None
    urgency: Optional[str] = None
    
    # Processing Status
    status: LeadStatus = LeadStatus.PENDING
    processing_stage: str = "received"
    error_message: Optional[str] = None
    
    # Company Intelligence
    company_data: Dict[str, Any] = Field(default_factory=dict)
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    funding_stage: Optional[str] = None
    revenue_range: Optional[str] = None
    
    # MEDDPICC Scoring
    meddpicc_score: Optional[MEDDPICCScore] = None
    
    # Pain Points
    pain_points: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    
    # Outreach Content
    personalized_emails: List[Dict[str, str]] = Field(default_factory=list)
    linkedin_message: Optional[str] = None
    
    # GTM Motion
    recommended_motion: Optional[GTM_Motion] = None
    motion_reasoning: Optional[str] = None
    
    # Case Study
    matched_case_study: Optional[Dict[str, Any]] = None
    
    # Decision Makers
    decision_makers: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Agent Logs
    agent_logs: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None
    qualified_at: Optional[datetime] = None
    
    @validator('email')
    def validate_email(cls, v):
        """Validate email format"""
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_qualified(self) -> bool:
        """Check if lead is qualified"""
        return self.status == LeadStatus.QUALIFIED
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True