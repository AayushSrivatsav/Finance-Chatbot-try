import os
import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from models.schemas import RAGQuery, RAGResponse

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.qa_chain = None
        self.memory = None
        self.collection = None
        self.chroma_client = None
        
    async def initialize(self):
        """Initialize the RAG service with embeddings and vector store"""
        try:
            # Initialize OpenAI embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                model="text-embedding-ada-002"
            )
            
            # Initialize ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path="./data/chroma_db",
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="finance_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            
            # Initialize LangChain vector store
            self.vectorstore = Chroma(
                client=self.chroma_client,
                collection_name="finance_knowledge",
                embedding_function=self.embeddings
            )
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                model="gpt-3.5-turbo",
                temperature=0.7
            )
            
            # Initialize memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Create QA chain
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 5}
                ),
                memory=self.memory,
                return_source_documents=True,
                verbose=True
            )
            
            logger.info("RAG service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG service: {e}")
            raise
    
    async def add_documents(self, documents: List[Document]):
        """Add documents to the vector store"""
        try:
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            
            chunks = text_splitter.split_documents(documents)
            
            # Add to vector store
            self.vectorstore.add_documents(chunks)
            
            logger.info(f"Added {len(chunks)} document chunks to vector store")
            return len(chunks)
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    async def process_query(self, query: str, conversation_id: Optional[str] = None) -> str:
        """Process a query using RAG"""
        try:
            start_time = datetime.now()
            
            # Process query through QA chain
            result = self.qa_chain({"question": query})
            
            # Extract answer and sources
            answer = result.get("answer", "I couldn't find a relevant answer.")
            source_documents = result.get("source_documents", [])
            
            # Format sources
            sources = []
            for doc in source_documents:
                sources.append({
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                })
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create response with sources
            response = {
                "answer": answer,
                "sources": sources,
                "processing_time": processing_time,
                "confidence": self._calculate_confidence(answer, sources)
            }
            
            logger.info(f"Processed query in {processing_time:.2f}s")
            return json.dumps(response)
            
        except Exception as e:
            logger.error(f"Failed to process query: {e}")
            return json.dumps({
                "answer": "I encountered an error while processing your query. Please try again.",
                "sources": [],
                "processing_time": 0,
                "confidence": 0.0
            })
    
    async def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            docs = self.vectorstore.similarity_search(query, k=top_k)
            
            results = []
            for doc in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": 0.8  # Placeholder score
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search similar documents: {e}")
            return []
    
    def _calculate_confidence(self, answer: str, sources: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on answer quality and sources"""
        if not sources:
            return 0.1
        
        # Simple confidence calculation
        base_confidence = 0.5
        source_bonus = min(len(sources) * 0.1, 0.3)
        answer_length_bonus = min(len(answer) / 1000, 0.2)
        
        return min(base_confidence + source_bonus + answer_length_bonus, 1.0)
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collection"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "embedding_model": "text-embedding-ada-002",
                "collection_name": "finance_knowledge"
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}
    
    async def clear_memory(self):
        """Clear conversation memory"""
        if self.memory:
            self.memory.clear()
            logger.info("Conversation memory cleared") 