from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AgentLog(BaseModel):
    """Agent execution log"""
    id: Optional[str] = None
    lead_id: str
    agent_name: str
    status: str  # success, error, running
    input_data: Dict[str, Any] = Field(default_factory=dict)
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AgentStatus(BaseModel):
    """Current agent status"""
    agent_name: str
    status: str  # idle, running, completed, error
    current_task: Optional[str] = None
    progress: float = 0.0  # 0-100
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    last_active: datetime = Field(default_factory=datetime.utcnow)