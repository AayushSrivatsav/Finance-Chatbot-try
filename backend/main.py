from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import json
from typing import List, Dict, Any
import logging

from routers import chat, news, stocks, rag
from services.websocket_manager import ConnectionManager
from services.news_scraper import NewsScraper
from services.rag_service import RAGService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Finance RAG Chatbot",
    description="A comprehensive RAG-powered finance chatbot with real-time news and stock analysis",
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

# WebSocket connection manager
manager = ConnectionManager()

# Initialize services
news_scraper = NewsScraper()
rag_service = RAGService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Finance RAG Chatbot...")
    await rag_service.initialize()
    logger.info("Services initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Finance RAG Chatbot...")

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(rag.router, prefix="/api/rag", tags=["rag"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Finance RAG Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "services": ["rag", "news", "stocks"]}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process message through RAG service
            response = await rag_service.process_query(message.get("message", ""))
            
            # Send response back to client
            await manager.send_personal_message(
                json.dumps({
                    "type": "response",
                    "message": response,
                    "timestamp": asyncio.get_event_loop().time()
                }),
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.send_personal_message(
            json.dumps({"type": "error", "message": "An error occurred"}),
            websocket
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 