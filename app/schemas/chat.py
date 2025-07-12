"""Chat schemas for API validation."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class MessageRoleEnum(str, Enum):
    """Message roles for chat history."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ContextTypeEnum(str, Enum):
    """Context types for enhanced context."""
    ONBOARDING = "onboarding"
    CONVERSATION = "conversation"
    PRODUCT_SEARCH = "product_search"
    RECOMMENDATION = "recommendation"


class ChatMessageBase(BaseModel):
    """Base chat message schema."""
    user_id: str = Field(..., description="User ID")
    session_id: str = Field(..., description="Session ID")
    content: str = Field(..., min_length=1, description="Message content")
    role: MessageRoleEnum = Field(default=MessageRoleEnum.USER, description="Message role")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Additional context data")


class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a chat message."""
    pass


class ChatMessageResponse(ChatMessageBase):
    """Schema for chat message responses."""
    id: int
    message_id: str
    tokens_used: Optional[int] = None
    response_time: Optional[int] = None
    model_used: Optional[str] = None
    processed: bool
    archived: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatThreadResponse(BaseModel):
    """Schema for chat thread responses."""
    session_id: str
    user_id: str
    messages: List[ChatMessageResponse]
    total_messages: int
    created_at: datetime
    last_activity: datetime
    summary: Optional[str] = None


class ChatThreadSummary(BaseModel):
    """Schema for chat thread summary."""
    session_id: str
    user_id: str
    message_count: int
    summary: str
    last_activity: datetime
    context_types: List[str]


class EnhancedContextBase(BaseModel):
    """Base enhanced context schema."""
    user_id: str = Field(..., description="User ID")
    context_type: ContextTypeEnum = Field(..., description="Context type")
    context_name: Optional[str] = Field(None, max_length=255, description="Context name")
    context_data: Optional[Dict[str, Any]] = Field(None, description="Context data")
    summary: Optional[str] = Field(None, description="Context summary")
    weight: int = Field(default=1, ge=1, le=10, description="Context weight")
    priority: int = Field(default=0, ge=0, le=10, description="Context priority")


class EnhancedContextCreate(EnhancedContextBase):
    """Schema for creating enhanced context."""
    session_id: Optional[str] = Field(None, description="Session ID (optional for global context)")


class EnhancedContextUpdate(BaseModel):
    """Schema for updating enhanced context."""
    context_name: Optional[str] = Field(None, max_length=255)
    context_data: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    weight: Optional[int] = Field(None, ge=1, le=10)
    priority: Optional[int] = Field(None, ge=0, le=10)
    active: Optional[bool] = None


class EnhancedContextResponse(EnhancedContextBase):
    """Schema for enhanced context responses."""
    id: int
    session_id: Optional[str] = None
    message_count: int
    last_activity: Optional[int] = None
    active: bool
    archived: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OnboardingRequest(BaseModel):
    """Schema for onboarding request."""
    user_id: str = Field(..., description="User ID")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    interests: Optional[List[str]] = Field(None, description="User interests")
    goals: Optional[List[str]] = Field(None, description="User goals")
    company_info: Optional[Dict[str, Any]] = Field(None, description="Company information")
    use_cases: Optional[List[str]] = Field(None, description="Use cases")


class OnboardingResponse(BaseModel):
    """Schema for onboarding response."""
    user_id: str
    context_id: int
    session_id: str
    welcome_message: str
    suggested_products: Optional[List[Dict[str, Any]]] = None
    next_steps: List[str]


class ChatRecommendationRequest(BaseModel):
    """Schema for chat-based recommendation request."""
    user_id: str = Field(..., description="User ID")
    session_id: Optional[str] = Field(None, description="Session ID")
    query: str = Field(..., min_length=1, description="User query")
    k: int = Field(default=5, ge=1, le=20, description="Number of recommendations")
    include_explanation: bool = Field(True, description="Include explanation")


class ChatRecommendationResponse(BaseModel):
    """Schema for chat-based recommendation response."""
    user_id: str
    session_id: str
    query: str
    recommendations: List[Dict[str, Any]]
    explanation: Optional[str] = None
    context_used: List[str]
    response_time: int


class ConversationAnalysis(BaseModel):
    """Schema for conversation analysis."""
    session_id: str
    user_id: str
    total_messages: int
    user_messages: int
    assistant_messages: int
    average_response_time: float
    total_tokens_used: int
    main_topics: List[str]
    sentiment_analysis: Dict[str, Any]
    user_satisfaction: Optional[float] = None
    recommendations_given: int
    products_mentioned: List[str]


class ChatMetrics(BaseModel):
    """Schema for chat metrics."""
    total_conversations: int
    active_conversations: int
    average_conversation_length: float
    total_messages: int
    average_response_time: float
    total_tokens_used: int
    user_satisfaction_score: Optional[float] = None
    top_topics: List[Dict[str, Any]]
    busiest_hours: List[Dict[str, Any]]


class ChatSearchRequest(BaseModel):
    """Schema for chat search request."""
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    session_id: Optional[str] = Field(None, description="Filter by session ID")
    query: Optional[str] = Field(None, description="Search query")
    role: Optional[MessageRoleEnum] = Field(None, description="Filter by message role")
    date_from: Optional[datetime] = Field(None, description="Date from")
    date_to: Optional[datetime] = Field(None, description="Date to")
    limit: int = Field(default=50, ge=1, le=1000, description="Limit results")


class ChatExportRequest(BaseModel):
    """Schema for chat export request."""
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    session_id: Optional[str] = Field(None, description="Filter by session ID")
    date_from: Optional[datetime] = Field(None, description="Date from")
    date_to: Optional[datetime] = Field(None, description="Date to")
    format: str = Field(default="json", pattern="^(json|csv|xlsx)$", description="Export format")
    include_context: bool = Field(True, description="Include context data")
    include_embeddings: bool = Field(False, description="Include embeddings")


class ChatCleanupRequest(BaseModel):
    """Schema for chat cleanup request."""
    older_than_days: int = Field(..., ge=1, le=365, description="Delete messages older than X days")
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    session_id: Optional[str] = Field(None, description="Filter by session ID")
    archive_only: bool = Field(True, description="Archive instead of delete")
    dry_run: bool = Field(True, description="Perform dry run first") 
