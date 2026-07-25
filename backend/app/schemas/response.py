from typing import Optional, Generic, TypeVar, Dict, Any, List
from pydantic import BaseModel, Field

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper"""
    status: str = Field(default="success")
    message: Optional[str] = None
    data: Optional[T] = None
    errors: Optional[List[Dict[str, Any]]] = None
    timestamp: str = Field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())


class SuccessResponse(BaseModel):
    """Success response schema"""
    status: str = "success"
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    status: str = "error"
    message: str
    error_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema"""
    data: List[T]
    pagination: Dict[str, Any] = Field(
        default_factory=lambda: {
            "total": 0,
            "skip": 0,
            "limit": 20,
            "pages": 0
        }
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: str = Field(default_factory=lambda: __import__('datetime').datetime.utcnow().isoformat())
    services: Dict[str, str] = Field(default_factory=dict)