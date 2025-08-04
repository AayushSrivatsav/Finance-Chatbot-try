from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    id: Optional[str] = None
    content: str = Field(..., min_length=1, max_length=1000)
    message_type: MessageType = MessageType.USER
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    timestamp: datetime
    sources: Optional[List[Dict[str, Any]]] = None
    confidence: Optional[float] = None

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    source: str
    published_at: Optional[datetime] = None
    sentiment: Optional[str] = None
    relevance_score: Optional[float] = None

class StockInfo(BaseModel):
    symbol: str
    name: str
    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    market_cap: Optional[float] = None
    volume: Optional[int] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None

class StockRecommendation(BaseModel):
    symbol: str
    recommendation: str  # "buy", "sell", "hold"
    confidence: float
    reasoning: str
    price_target: Optional[float] = None
    risk_level: str = "medium"
    news_sentiment: Optional[str] = None

class NewsRequest(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)
    sources: Optional[List[str]] = None

class RAGQuery(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    include_sources: bool = True

class RAGResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    processing_time: float

class WebSocketMessage(BaseModel):
    type: str  # "message", "typing", "error"
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthCheck(BaseModel):
    status: str
    services: List[str]
    timestamp: datetime = Field(default_factory=datetime.now) 