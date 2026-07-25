from fastapi import APIRouter

from app.api.endspoints import leads, analysis, agents

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
