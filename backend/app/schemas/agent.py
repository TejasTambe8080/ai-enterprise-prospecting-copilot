from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field


class AgentStatusResponse(BaseModel):
    """Schema for agent status response"""
    agent_name: str
    status: str  # idle, running, completed, error
    current_task: Optional[str] = None
    progress: float = Field(default=0.0, ge=0, le=100)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    last_active: datetime = Field(default_factory=datetime.utcnow)


class AgentLogResponse(BaseModel):
    """Schema for agent log response"""
    id: Optional[str] = None
    lead_id: str
    agent_name: str
    status: str
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentListResponse(BaseModel):
    """Schema for list of agent statuses"""
    agents: Dict[str, AgentStatusResponse]
    total_agents: int
    active_agents: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)