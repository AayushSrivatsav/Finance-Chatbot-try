from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import json
import logging

from models.schemas import ChatRequest, ChatResponse, ChatMessage
from services.rag_service import RAGService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize RAG service
rag_service = RAGService()

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a chat message and get AI response"""
    try:
        # Process message through RAG service
        response_data = await rag_service.process_query(request.message, request.conversation_id)
        
        # Parse the JSON response
        response_dict = json.loads(response_data)
        
        return ChatResponse(
            message=response_dict.get("answer", "I couldn't process your request."),
            conversation_id=request.conversation_id or "default",
            timestamp=response_dict.get("timestamp"),
            sources=response_dict.get("sources"),
            confidence=response_dict.get("confidence")
        )
        
    except Exception as e:
        logger.error(f"Failed to process chat message: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message")

@router.get("/history/{conversation_id}", response_model=List[ChatMessage])
async def get_conversation_history(conversation_id: str):
    """Get conversation history for a specific conversation"""
    try:
        # In a real implementation, you'd fetch from a database
        # For now, return empty list
        return []
        
    except Exception as e:
        logger.error(f"Failed to get conversation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation history")

@router.delete("/history/{conversation_id}")
async def clear_conversation_history(conversation_id: str):
    """Clear conversation history"""
    try:
        # Clear memory for the conversation
        await rag_service.clear_memory()
        return {"message": "Conversation history cleared"}
        
    except Exception as e:
        logger.error(f"Failed to clear conversation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear conversation history")

@router.get("/stats")
async def get_chat_stats():
    """Get chat statistics"""
    try:
        stats = await rag_service.get_collection_stats()
        return {
            "total_conversations": 1,  # Placeholder
            "total_messages": 0,  # Placeholder
            "rag_stats": stats
        }
        
    except Exception as e:
        logger.error(f"Failed to get chat stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get chat stats") 