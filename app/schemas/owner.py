"""Owner schemas for API validation."""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum


class SolutionOwnerBase(BaseModel):
    """Base schema for solution owner."""
    name: str = Field(..., min_length=1, max_length=255, description="Company name")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', description="Company email")
    website: Optional[str] = Field(None, max_length=500, description="Company website")
    description: Optional[str] = Field(None, max_length=2000, description="Company description")
    
    # Contact information
    contact_name: Optional[str] = Field(None, max_length=255, description="Contact person name")
    contact_phone: Optional[str] = Field(None, max_length=50, description="Contact phone")
    contact_email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', description="Contact email")
    
    # Business information
    industry: Optional[str] = Field(None, max_length=100, description="Industry sector")
    company_size: Optional[str] = Field(None, max_length=50, description="Company size")
    location: Optional[str] = Field(None, max_length=255, description="Company location")
    founded_year: Optional[int] = Field(None, ge=1800, le=2024, description="Year founded")
    
    # Additional metadata
    logo_url: Optional[str] = Field(None, max_length=500, description="Logo URL")
    tags: Optional[List[str]] = Field(default_factory=list, description="Company tags")
    is_verified: bool = Field(default=False, description="Verification status")

    @validator('website', 'logo_url')
    def validate_url(cls, v):
        """Validate URL format."""
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v

    @validator('tags')
    def validate_tags(cls, v):
        """Validate tags list."""
        if v and len(v) > 20:
            raise ValueError('Maximum 20 tags allowed')
        return v


class SolutionOwnerCreate(SolutionOwnerBase):
    """Schema for creating a solution owner."""
    pass


class SolutionOwnerUpdate(BaseModel):
    """Schema for updating a solution owner."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    website: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    contact_name: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=50)
    contact_email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    industry: Optional[str] = Field(None, max_length=100)
    company_size: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    founded_year: Optional[int] = Field(None, ge=1800, le=2024)
    logo_url: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(None)
    is_verified: Optional[bool] = None

    @validator('website', 'logo_url')
    def validate_url(cls, v):
        """Validate URL format."""
        if v and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v


class SolutionOwnerResponse(SolutionOwnerBase):
    """Schema for solution owner response."""
    id: int
    created_at: datetime
    updated_at: datetime
    products_count: int = Field(default=0, description="Number of products")
    
    # Computed fields
    verification_status: str = Field(default="pending", description="Verification status")
    profile_completeness: float = Field(default=0.0, ge=0.0, le=1.0, description="Profile completeness score")

    class Config:
        from_attributes = True

    @validator('email')
    def mask_email(cls, v):
        """Mask email for privacy."""
        if '@' in v:
            local, domain = v.split('@', 1)
            if len(local) > 2:
                masked_local = local[:2] + '*' * (len(local) - 2)
                return f"{masked_local}@{domain}"
        return v


class SolutionOwnerListResponse(BaseModel):
    """Schema for paginated solution owner list."""
    owners: List[SolutionOwnerResponse]
    total: int
    page: int
    size: int
    pages: int


class SolutionOwnerSearchParams(BaseModel):
    """Schema for solution owner search parameters."""
    q: Optional[str] = Field(None, description="Search query")
    industry: Optional[str] = Field(None, description="Filter by industry")
    company_size: Optional[str] = Field(None, description="Filter by company size")
    location: Optional[str] = Field(None, description="Filter by location")
    is_verified: Optional[bool] = Field(None, description="Filter by verification status")
    founded_after: Optional[int] = Field(None, ge=1800, description="Founded after year")
    founded_before: Optional[int] = Field(None, le=2024, description="Founded before year")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    sort_by: Optional[str] = Field("created_at", description="Sort field")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$", description="Sort order")
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(20, ge=1, le=100, description="Page size") 
