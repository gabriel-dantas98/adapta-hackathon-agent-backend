"""Chat and context models."""

from typing import List, Optional
from sqlalchemy import Column, String, Text, Boolean, Integer, UUID, JSON, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from pgvector.sqlalchemy import Vector
import uuid
import enum

from app.models.base import BaseModel


class MessageRole(str, enum.Enum):
    """Message roles for chat history."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ContextType(str, enum.Enum):
    """Context types for enhanced context."""
    ONBOARDING = "onboarding"
    CONVERSATION = "conversation"
    PRODUCT_SEARCH = "product_search"
    RECOMMENDATION = "recommendation"


class UserChatHistory(BaseModel):
    """User chat history model."""
    
    __tablename__ = "users_chat_history"
    
    # User identification
    user_id = Column(String(255), nullable=False, index=True)
    session_id = Column(String(255), nullable=False, index=True)
    
    # Message details
    message_id = Column(PostgresUUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    role = Column(SqlEnum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    
    # Context
    context_data = Column(JSON)  # Additional context data
    tokens_used = Column(Integer)  # Token count for the message
    
    # Vector embedding for similarity search
    embeddings = Column(Vector(1536), nullable=True)
    
    # Message metadata
    response_time = Column(Integer)  # Response time in milliseconds
    model_used = Column(String(100))  # Model used for response
    
    # Status
    processed = Column(Boolean, default=False, nullable=False)
    archived = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<UserChatHistory(id={self.id}, user_id={self.user_id}, role={self.role})>"
    
    def to_text_for_embedding(self) -> str:
        """Convert message to text for embedding generation."""
        parts = [f"Role: {self.role.value}", f"Content: {self.content}"]
        
        if self.context_data:
            context_text = str(self.context_data)
            parts.append(f"Context: {context_text}")
        
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "message_id": str(self.message_id),
            "role": self.role.value,
            "content": self.content,
            "context_data": self.context_data,
            "tokens_used": self.tokens_used,
            "response_time": self.response_time,
            "model_used": self.model_used,
            "processed": self.processed,
            "archived": self.archived,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class UserEnhancedContext(BaseModel):
    """User enhanced context model for maintaining conversation state."""
    
    __tablename__ = "users_enhanced_context"
    
    # User identification
    user_id = Column(String(255), nullable=False, index=True)
    session_id = Column(String(255), nullable=True, index=True)  # Can be null for global context
    
    # Context details
    context_type = Column(SqlEnum(ContextType), nullable=False)
    context_name = Column(String(255))  # Name/title for the context
    
    # Context data
    context_data = Column(JSON)  # Structured context data
    summary = Column(Text)  # Human-readable summary
    
    # Vector embeddings
    embeddings = Column(Vector(1536), nullable=True)
    
    # Metadata
    message_count = Column(Integer, default=0)  # Number of messages in this context
    last_activity = Column(Integer)  # Unix timestamp of last activity
    
    # Weights for context combination
    weight = Column(Integer, default=1)  # Weight for combining contexts
    priority = Column(Integer, default=0)  # Priority for context selection
    
    # Status
    active = Column(Boolean, default=True, nullable=False)
    archived = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<UserEnhancedContext(id={self.id}, user_id={self.user_id}, type={self.context_type})>"
    
    def to_text_for_embedding(self) -> str:
        """Convert context to text for embedding generation."""
        parts = [f"Type: {self.context_type.value}"]
        
        if self.context_name:
            parts.append(f"Name: {self.context_name}")
        
        if self.summary:
            parts.append(f"Summary: {self.summary}")
        
        if self.context_data:
            # Extract useful information from context_data
            if isinstance(self.context_data, dict):
                for key, value in self.context_data.items():
                    if key in ['preferences', 'interests', 'goals', 'requirements']:
                        parts.append(f"{key.title()}: {value}")
        
        return " | ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "context_type": self.context_type.value,
            "context_name": self.context_name,
            "context_data": self.context_data,
            "summary": self.summary,
            "message_count": self.message_count,
            "last_activity": self.last_activity,
            "weight": self.weight,
            "priority": self.priority,
            "active": self.active,
            "archived": self.archived,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def update_activity(self):
        """Update last activity timestamp."""
        import time
        self.last_activity = int(time.time())
    
    def increment_message_count(self):
        """Increment message count."""
        self.message_count = (self.message_count or 0) + 1 
