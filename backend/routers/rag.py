from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
import logging
import json

from models.schemas import RAGQuery, RAGResponse
from services.rag_service import RAGService
from langchain.schema import Document

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize RAG service
rag_service = RAGService()

@router.post("/query", response_model=RAGResponse)
async def query_rag(request: RAGQuery):
    """Query the RAG system"""
    try:
        # Process query through RAG service
        response_data = await rag_service.process_query(request.query)
        
        # Parse the JSON response
        response_dict = json.loads(response_data)
        
        return RAGResponse(
            answer=response_dict.get("answer", "No answer found"),
            sources=response_dict.get("sources", []),
            confidence=response_dict.get("confidence", 0.0),
            processing_time=response_dict.get("processing_time", 0.0)
        )
        
    except Exception as e:
        logger.error(f"Failed to process RAG query: {e}")
        raise HTTPException(status_code=500, detail="Failed to process query")

@router.get("/search")
async def search_similar(query: str, top_k: int = 5):
    """Search for similar documents"""
    try:
        results = await rag_service.search_similar(query, top_k)
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Failed to search similar documents: {e}")
        raise HTTPException(status_code=500, detail="Failed to search documents")

@router.get("/stats")
async def get_rag_stats():
    """Get RAG system statistics"""
    try:
        stats = await rag_service.get_collection_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get RAG stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get RAG statistics")

@router.post("/add-documents")
async def add_documents(file: UploadFile = File(...)):
    """Add documents to the RAG system"""
    try:
        # Read file content
        content = await file.read()
        text_content = content.decode('utf-8')
        
        # Create document
        document = Document(
            page_content=text_content,
            metadata={
                "source": file.filename,
                "type": "uploaded_file",
                "size": len(text_content)
            }
        )
        
        # Add to RAG system
        chunks_added = await rag_service.add_documents([document])
        
        return {
            "message": f"Successfully added document",
            "chunks_added": chunks_added,
            "filename": file.filename
        }
        
    except Exception as e:
        logger.error(f"Failed to add document: {e}")
        raise HTTPException(status_code=500, detail="Failed to add document")

@router.post("/add-text")
async def add_text(text: str, metadata: Optional[dict] = None):
    """Add text content to the RAG system"""
    try:
        # Create document
        document = Document(
            page_content=text,
            metadata=metadata or {
                "type": "text_input",
                "size": len(text)
            }
        )
        
        # Add to RAG system
        chunks_added = await rag_service.add_documents([document])
        
        return {
            "message": "Successfully added text content",
            "chunks_added": chunks_added
        }
        
    except Exception as e:
        logger.error(f"Failed to add text: {e}")
        raise HTTPException(status_code=500, detail="Failed to add text content")

@router.delete("/clear")
async def clear_rag_system():
    """Clear the RAG system (reset vector database)"""
    try:
        # Clear memory
        await rag_service.clear_memory()
        
        return {"message": "RAG system cleared successfully"}
        
    except Exception as e:
        logger.error(f"Failed to clear RAG system: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear RAG system")

@router.get("/health")
async def rag_health_check():
    """Health check for RAG system"""
    try:
        stats = await rag_service.get_collection_stats()
        return {
            "status": "healthy",
            "collection_stats": stats,
            "service": "RAG"
        }
        
    except Exception as e:
        logger.error(f"RAG health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "service": "RAG"
        } 