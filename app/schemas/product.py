"""Product schemas for API validation."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    subcategory: Optional[str] = Field(None, max_length=100, description="Product subcategory")
    
    # Product details
    version: Optional[str] = Field(None, max_length=50, description="Product version")
    price: Optional[Decimal] = Field(None, ge=0, description="Product price")
    pricing_model: Optional[str] = Field(None, max_length=50, description="Pricing model")
    currency: Optional[str] = Field("USD", max_length=10, description="Currency")
    
    # Technical details
    platform: Optional[str] = Field(None, max_length=100, description="Platform")
    integrations: Optional[List[str]] = Field(None, description="List of integrations")
    features: Optional[List[str]] = Field(None, description="List of features")
    tech_stack: Optional[List[str]] = Field(None, description="Technology stack")
    
    # Availability
    demo_available: bool = Field(False, description="Demo available")
    trial_available: bool = Field(False, description="Trial available")
    
    # URLs
    website_url: Optional[str] = Field(None, max_length=500, description="Website URL")
    demo_url: Optional[str] = Field(None, max_length=500, description="Demo URL")
    documentation_url: Optional[str] = Field(None, max_length=500, description="Documentation URL")
    
    # Search metadata
    search_keywords: Optional[str] = Field(None, description="Search keywords")
    use_cases: Optional[List[str]] = Field(None, description="Use cases")
    target_audience: Optional[str] = Field(None, max_length=255, description="Target audience")
    
    @validator('pricing_model')
    def validate_pricing_model(cls, v):
        if v is not None:
            allowed_models = ['One-time', 'Monthly', 'Yearly', 'Usage-based', 'Freemium']
            if v not in allowed_models:
                raise ValueError(f'Pricing model must be one of: {", ".join(allowed_models)}')
        return v
    
    @validator('currency')
    def validate_currency(cls, v):
        if v is not None:
            allowed_currencies = ['USD', 'EUR', 'GBP', 'BRL', 'CAD', 'AUD']
            if v not in allowed_currencies:
                raise ValueError(f'Currency must be one of: {", ".join(allowed_currencies)}')
        return v
    
    @validator('platform')
    def validate_platform(cls, v):
        if v is not None:
            allowed_platforms = ['Web', 'Mobile', 'Desktop', 'API', 'Cloud', 'On-premise']
            if v not in allowed_platforms:
                raise ValueError(f'Platform must be one of: {", ".join(allowed_platforms)}')
        return v
    
    @validator('website_url', 'demo_url', 'documentation_url')
    def validate_url(cls, v):
        if v is not None and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    owner_id: int = Field(..., description="Owner ID")


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    version: Optional[str] = Field(None, max_length=50)
    price: Optional[Decimal] = Field(None, ge=0)
    pricing_model: Optional[str] = Field(None, max_length=50)
    currency: Optional[str] = Field(None, max_length=10)
    platform: Optional[str] = Field(None, max_length=100)
    integrations: Optional[List[str]] = None
    features: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    available: Optional[bool] = None
    demo_available: Optional[bool] = None
    trial_available: Optional[bool] = None
    website_url: Optional[str] = Field(None, max_length=500)
    demo_url: Optional[str] = Field(None, max_length=500)
    documentation_url: Optional[str] = Field(None, max_length=500)
    search_keywords: Optional[str] = None
    use_cases: Optional[List[str]] = None
    target_audience: Optional[str] = Field(None, max_length=255)
    
    @validator('pricing_model')
    def validate_pricing_model(cls, v):
        if v is not None:
            allowed_models = ['One-time', 'Monthly', 'Yearly', 'Usage-based', 'Freemium']
            if v not in allowed_models:
                raise ValueError(f'Pricing model must be one of: {", ".join(allowed_models)}')
        return v
    
    @validator('currency')
    def validate_currency(cls, v):
        if v is not None:
            allowed_currencies = ['USD', 'EUR', 'GBP', 'BRL', 'CAD', 'AUD']
            if v not in allowed_currencies:
                raise ValueError(f'Currency must be one of: {", ".join(allowed_currencies)}')
        return v
    
    @validator('platform')
    def validate_platform(cls, v):
        if v is not None:
            allowed_platforms = ['Web', 'Mobile', 'Desktop', 'API', 'Cloud', 'On-premise']
            if v not in allowed_platforms:
                raise ValueError(f'Platform must be one of: {", ".join(allowed_platforms)}')
        return v
    
    @validator('website_url', 'demo_url', 'documentation_url')
    def validate_url(cls, v):
        if v is not None and not v.startswith(('http://', 'https://')):
            return f'https://{v}'
        return v


class ProductResponse(ProductBase):
    """Schema for product responses."""
    id: int
    owner_id: int
    available: bool
    rating: Optional[float] = None
    total_reviews: int
    popularity_score: Optional[float] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductWithOwner(ProductResponse):
    """Schema for product with owner information."""
    owner: Dict[str, Any]
    
    class Config:
        from_attributes = True


class ProductList(BaseModel):
    """Schema for product list responses."""
    id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    owner_id: int
    price: Optional[float] = None
    pricing_model: Optional[str] = None
    currency: Optional[str] = None
    platform: Optional[str] = None
    rating: Optional[float] = None
    available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductSearch(BaseModel):
    """Schema for product search."""
    query: Optional[str] = Field(None, description="Search query")
    category: Optional[str] = Field(None, description="Filter by category")
    subcategory: Optional[str] = Field(None, description="Filter by subcategory")
    platform: Optional[str] = Field(None, description="Filter by platform")
    pricing_model: Optional[str] = Field(None, description="Filter by pricing model")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")
    demo_available: Optional[bool] = Field(None, description="Demo available")
    trial_available: Optional[bool] = Field(None, description="Trial available")
    available_only: bool = Field(True, description="Only show available products")
    
    @validator('pricing_model')
    def validate_pricing_model(cls, v):
        if v is not None:
            allowed_models = ['One-time', 'Monthly', 'Yearly', 'Usage-based', 'Freemium']
            if v not in allowed_models:
                raise ValueError(f'Pricing model must be one of: {", ".join(allowed_models)}')
        return v
    
    @validator('platform')
    def validate_platform(cls, v):
        if v is not None:
            allowed_platforms = ['Web', 'Mobile', 'Desktop', 'API', 'Cloud', 'On-premise']
            if v not in allowed_platforms:
                raise ValueError(f'Platform must be one of: {", ".join(allowed_platforms)}')
        return v


class ProductRecommendation(BaseModel):
    """Schema for product recommendations."""
    user_id: str = Field(..., description="User ID")
    k: int = Field(default=5, ge=1, le=50, description="Number of recommendations")
    include_owned: bool = Field(False, description="Include products from same owner")
    category_filter: Optional[str] = Field(None, description="Filter by category")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating")


class ProductRecommendationResult(BaseModel):
    """Schema for product recommendation results."""
    product: ProductResponse
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    reason: Optional[str] = None


class ProductBulkCreate(BaseModel):
    """Schema for bulk creating products."""
    products: List[ProductCreate] = Field(..., min_items=1, max_items=50)


class ProductStats(BaseModel):
    """Schema for product statistics."""
    total_products: int
    available_products: int
    by_category: Dict[str, int]
    by_platform: Dict[str, int]
    by_pricing_model: Dict[str, int]
    average_rating: float
    recent_products: int 
