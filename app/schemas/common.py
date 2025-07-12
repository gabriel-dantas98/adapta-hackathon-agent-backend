"""Common schemas and response models."""

from typing import Any, Dict, List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime


T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None
    errors: Optional[List[str]] = None


class PaginatedResponse(BaseResponse, Generic[T]):
    """Paginated response model."""
    data: List[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 10
    total_pages: int = 0
    has_next: bool = False
    has_prev: bool = False


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=10, ge=1, le=100, description="Items per page")


class SearchParams(BaseModel):
    """Search parameters."""
    q: Optional[str] = Field(None, description="Search query")
    sort_by: Optional[str] = Field(None, description="Sort field")
    sort_order: Optional[str] = Field("asc", pattern="^(asc|desc)$", description="Sort order")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    services: Dict[str, str]
    version: str


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    message: str
    errors: List[str] = Field(default_factory=list)
    error_code: Optional[str] = None
    request_id: Optional[str] = None


class VectorSimilarity(BaseModel):
    """Vector similarity result."""
    item_id: int
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    item_data: Optional[Dict[str, Any]] = None


class EmbeddingStats(BaseModel):
    """Embedding service statistics."""
    cache_size: int
    max_cache_size: int
    hit_rate: str
    memory_usage: str 
