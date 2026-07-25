from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.agents.orchestrator import AgentOrchestrator

router = APIRouter()

@router.post("/analyze")
async def analyze_company(company_name: str) -> Dict[str, Any]:
    """Analyze a company and provide insights"""
    try:
        # Create orchestrator
        orchestrator = AgentOrchestrator()
        
        # Use research agents
        research_agent = orchestrator.agents["company_research"]
        result = await research_agent.run({
            "company": company_name,
            "domain": ""
        })
        
        return {
            "status": "success",
            "data": result.get("data", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))