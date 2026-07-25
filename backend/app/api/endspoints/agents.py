from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter()

@router.get("/status")
async def get_agent_status() -> Dict[str, Any]:
    """Get status of all agents"""
    try:
        # Create orchestrator
        orchestrator = AgentOrchestrator()
        
        status = {
            agent_name: agent.status
            for agent_name, agent in orchestrator.agents.items()
        }
        
        return {
            "status": "success",
            "data": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))