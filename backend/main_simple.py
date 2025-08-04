from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import List, Optional
import json

app = FastAPI(
    title="Finance RAG Chatbot API",
    description="AI-powered financial assistant with RAG capabilities",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[dict] = []
    confidence: float = 0.8

class NewsArticle(BaseModel):
    title: str
    description: str
    url: str
    published_at: str
    source: str
    sentiment: str = "neutral"

# Mock data
MOCK_NEWS = [
    {
        "title": "Tech Stocks Rally on Strong Earnings",
        "description": "Major technology companies report better-than-expected quarterly results, driving market optimism.",
        "url": "https://example.com/tech-rally",
        "published_at": "2024-08-04T10:00:00Z",
        "source": "Reuters",
        "sentiment": "positive"
    },
    {
        "title": "Federal Reserve Signals Potential Rate Changes",
        "description": "The Fed indicates possible adjustments to interest rates in response to economic indicators.",
        "url": "https://example.com/fed-rates",
        "published_at": "2024-08-04T09:30:00Z",
        "source": "Bloomberg",
        "sentiment": "neutral"
    }
]

@app.get("/")
async def root():
    return {"message": "Finance RAG Chatbot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

@app.post("/chat/send", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    """Send a chat message and get AI response"""
    # Simple mock response
    if "stock" in message.message.lower():
        response = "Based on current market analysis, I recommend focusing on technology and healthcare sectors. Consider diversifying your portfolio with ETFs like QQQ and VHT."
    elif "news" in message.message.lower():
        response = "Here are the latest financial headlines: Tech stocks are rallying on strong earnings, and the Federal Reserve is signaling potential rate changes."
    else:
        response = "I'm your AI financial assistant! I can help you with stock analysis, market news, and investment recommendations. What would you like to know?"
    
    return ChatResponse(
        response=response,
        sources=[{"title": "Market Analysis", "url": "https://example.com"}],
        confidence=0.85
    )

@app.get("/news/latest")
async def get_latest_news():
    """Get latest financial news"""
    return MOCK_NEWS

@app.get("/news/stock/{symbol}")
async def get_stock_news(symbol: str):
    """Get news for a specific stock"""
    return [article for article in MOCK_NEWS if symbol.lower() in article["title"].lower()]

@app.get("/stocks/info/{symbol}")
async def get_stock_info(symbol: str):
    """Get stock information"""
    return {
        "symbol": symbol.upper(),
        "name": f"{symbol.upper()} Corporation",
        "price": 150.25,
        "change": 2.5,
        "change_percent": 1.67,
        "market_cap": "2.5T",
        "volume": "50M"
    }

@app.get("/stocks/recommendation/{symbol}")
async def get_stock_recommendation(symbol: str):
    """Get AI stock recommendation"""
    return {
        "symbol": symbol.upper(),
        "recommendation": "BUY",
        "confidence": 0.75,
        "reasoning": "Strong fundamentals, positive technical indicators, and favorable market conditions.",
        "price_target": 165.00,
        "risk_level": "Medium"
    }

if __name__ == "__main__":
    print("🚀 Starting Finance RAG Chatbot API (Simple Mode)...")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False) 