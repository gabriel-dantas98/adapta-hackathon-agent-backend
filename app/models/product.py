"""Product model."""

from typing import List, Optional
from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.models.base import BaseModel


class Product(BaseModel):
    """Product model with embeddings support."""
    
    __tablename__ = "products"
    
    # Basic fields
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100))
    subcategory = Column(String(100))
    
    # Owner relationship
    owner_id = Column(Integer, ForeignKey("solutions_owner.id"), nullable=False)
    owner = relationship("SolutionOwner", back_populates="products")
    
    # Product details
    version = Column(String(50))
    price = Column(Numeric(10, 2))
    pricing_model = Column(String(50))  # One-time, Monthly, Yearly, Usage-based
    currency = Column(String(10), default="USD")
    
    # Technical details
    platform = Column(String(100))  # Web, Mobile, Desktop, API
    integrations = Column(JSON)  # List of integrations
    features = Column(JSON)  # List of features
    tech_stack = Column(JSON)  # Technologies used
    
    # Availability
    available = Column(Boolean, default=True, nullable=False)
    demo_available = Column(Boolean, default=False, nullable=False)
    trial_available = Column(Boolean, default=False, nullable=False)
    
    # URLs
    website_url = Column(String(500))
    demo_url = Column(String(500))
    documentation_url = Column(String(500))
    
    # Ratings and metrics
    rating = Column(Numeric(3, 2))  # 0.00 to 5.00
    total_reviews = Column(Integer, default=0)
    popularity_score = Column(Numeric(5, 2))  # Internal scoring
    
    # Vector embedding for similarity search
    embeddings = Column(Vector(1536), nullable=True)
    
    # Search metadata
    search_keywords = Column(Text)  # Keywords for search optimization
    summary = Column(Text)  # AI-generated summary
    use_cases = Column(JSON)  # List of use cases
    target_audience = Column(String(255))
    
    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, owner_id={self.owner_id})>"
    
    def to_text_for_embedding(self) -> str:
        """Convert product data to text for embedding generation."""
        parts = []
        
        if self.name:
            parts.append(f"Product: {self.name}")
        
        if self.description:
            parts.append(f"Description: {self.description}")
        
        if self.category:
            parts.append(f"Category: {self.category}")
        
        if self.subcategory:
            parts.append(f"Subcategory: {self.subcategory}")
        
        if self.platform:
            parts.append(f"Platform: {self.platform}")
        
        if self.features:
            features_text = ", ".join(self.features) if isinstance(self.features, list) else str(self.features)
            parts.append(f"Features: {features_text}")
        
        if self.tech_stack:
            tech_text = ", ".join(self.tech_stack) if isinstance(self.tech_stack, list) else str(self.tech_stack)
            parts.append(f"Technology: {tech_text}")
        
        if self.use_cases:
            use_cases_text = ", ".join(self.use_cases) if isinstance(self.use_cases, list) else str(self.use_cases)
            parts.append(f"Use Cases: {use_cases_text}")
        
        if self.target_audience:
            parts.append(f"Target Audience: {self.target_audience}")
        
        if self.search_keywords:
            parts.append(f"Keywords: {self.search_keywords}")
        
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        
        # Include owner context
        if self.owner:
            parts.append(f"Company: {self.owner.name}")
            if self.owner.industry:
                parts.append(f"Industry: {self.owner.industry}")
        
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "owner_id": self.owner_id,
            "version": self.version,
            "price": float(self.price) if self.price else None,
            "pricing_model": self.pricing_model,
            "currency": self.currency,
            "platform": self.platform,
            "integrations": self.integrations,
            "features": self.features,
            "tech_stack": self.tech_stack,
            "available": self.available,
            "demo_available": self.demo_available,
            "trial_available": self.trial_available,
            "website_url": self.website_url,
            "demo_url": self.demo_url,
            "documentation_url": self.documentation_url,
            "rating": float(self.rating) if self.rating else None,
            "total_reviews": self.total_reviews,
            "popularity_score": float(self.popularity_score) if self.popularity_score else None,
            "search_keywords": self.search_keywords,
            "summary": self.summary,
            "use_cases": self.use_cases,
            "target_audience": self.target_audience,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def to_dict_with_owner(self) -> dict:
        """Convert to dictionary including owner information."""
        data = self.to_dict()
        if self.owner:
            data["owner"] = self.owner.to_dict()
        return data 
