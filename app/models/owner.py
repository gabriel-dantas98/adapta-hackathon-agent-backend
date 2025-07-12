"""Solution owner model."""

from typing import List, Optional
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid

from app.models.base import BaseModel


class SolutionOwner(BaseModel):
    """Solution owner model with embeddings support."""
    
    __tablename__ = "solutions_owner"
    
    # Basic fields
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    website = Column(String(255))
    industry = Column(String(100))
    size = Column(String(50))  # Small, Medium, Large, Enterprise
    location = Column(String(100))
    
    # Contact information
    contact_name = Column(String(255))
    contact_phone = Column(String(50))
    contact_email = Column(String(255))
    
    # Status
    active = Column(Boolean, default=True, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    
    # Vector embedding for similarity search
    embeddings = Column(Vector(1536), nullable=True)
    
    # Search metadata
    search_keywords = Column(Text)  # Keywords for search optimization
    summary = Column(Text)  # AI-generated summary
    
    # Relationships
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<SolutionOwner(id={self.id}, name={self.name}, email={self.email})>"
    
    def to_text_for_embedding(self) -> str:
        """Convert owner data to text for embedding generation."""
        parts = []
        
        if self.name:
            parts.append(f"Company: {self.name}")
        
        if self.description:
            parts.append(f"Description: {self.description}")
        
        if self.industry:
            parts.append(f"Industry: {self.industry}")
        
        if self.size:
            parts.append(f"Size: {self.size}")
        
        if self.location:
            parts.append(f"Location: {self.location}")
        
        if self.search_keywords:
            parts.append(f"Keywords: {self.search_keywords}")
        
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "description": self.description,
            "website": self.website,
            "industry": self.industry,
            "size": self.size,
            "location": self.location,
            "contact_name": self.contact_name,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "active": self.active,
            "verified": self.verified,
            "search_keywords": self.search_keywords,
            "summary": self.summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 
