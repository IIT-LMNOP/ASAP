# main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import uvicorn
import logging
from contextlib import asynccontextmanager

# Import our RAG service
from chatbot import AlumniRAGService
rag_service = AlumniRAGService()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="Question about alumni")
    session_id: Optional[str] = Field(default="default", description="Session ID for conversation history")

class QueryResponse(BaseModel):
    success: bool
    answer: str
    session_id: str
    error: Optional[str] = None

class AddAlumniRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    profession: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    graduation_year: Optional[int] = Field(None, ge=1950, le=2030)
    degree: Optional[str] = None
    department: Optional[str] = None
    skills: Optional[List[str]] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

class AddAlumniResponse(BaseModel):
    success: bool
    alumni_id: Optional[str] = None
    message: str
    error: Optional[str] = None

class ConversationMessage(BaseModel):
    type: str  # "human" or "ai"
    content: str

class ConversationHistoryResponse(BaseModel):
    success: bool
    session_id: str
    messages: List[ConversationMessage]

class HealthCheckResponse(BaseModel):
    status: str
    mongodb: str
    vectorstore: str
    total_documents: int
    active_sessions: int

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Alumni RAG API...")
    try:
        # The service is already initialized when imported
        health = rag_service.health_check()
        logger.info(f"Service health check: {health}")
        logger.info("Alumni RAG API started successfully")
    except Exception as e:
        logger.error(f"Failed to start service: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Alumni RAG API...")

# Create FastAPI app
app = FastAPI(
    title="Alumni RAG API",
    description="AI-powered question answering system for Alumni Management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query", response_model=QueryResponse)
async def query_alumni(request: QueryRequest):
    """
    Query the alumni database using natural language
    
    - **question**: Natural language question about alumni
    - **session_id**: Optional session ID to maintain conversation context
    """
    try:
        logger.info(f"Processing query: {request.question[:50]}...")
        
        result = rag_service.query_alumni(
            question=request.question,
            session_id=request.session_id
        )

        return QueryResponse(
            success=result["success"],
            answer=result["answer"],
            session_id=request.session_id,
            error=result.get("error")
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/alumni", response_model=AddAlumniResponse)
async def add_alumni(request: AddAlumniRequest, background_tasks: BackgroundTasks):
    """
    Add a new alumni to the database and update embeddings
    
    This endpoint adds the alumni to MongoDB and automatically updates
    the vector embeddings for immediate searchability.
    """
    try:
        logger.info(f"Adding new alumni: {request.name}")
        
        # Convert request to dict, excluding None values
        alumni_data = request.model_dump(exclude_none=True)
        
        # If additional_info is provided, merge it into the main document
        if alumni_data.get('additional_info'):
            additional_info = alumni_data.pop('additional_info')
            alumni_data.update(additional_info)
        
        # Add alumni and embed
        alumni_id = rag_service.add_alumni_and_embed(alumni_data)
        
        return AddAlumniResponse(
            success=True,
            alumni_id=alumni_id,
            message=f"Alumni {request.name} added successfully and embedded for search"
        )
        
    except Exception as e:
        logger.error(f"Error adding alumni: {e}")
        return AddAlumniResponse(
            success=False,
            message="Failed to add alumni",
            error=str(e)
        )

@app.get("/conversation/{session_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(session_id: str):
    """
    Get conversation history for a specific session
    """
    try:
        messages = rag_service.get_conversation_history(session_id)
        
        return ConversationHistoryResponse(
            success=True,
            session_id=session_id,
            messages=[ConversationMessage(**msg) for msg in messages]
        )
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversation/{session_id}")
async def clear_conversation(session_id: str):
    """
    Clear conversation history for a specific session
    """
    try:
        success = rag_service.clear_conversation(session_id)
        
        if success:
            return {"message": f"Conversation history cleared for session: {session_id}"}
        else:
            return {"message": f"No conversation found for session: {session_id}"}
            
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update-embeddings")
async def force_update_embeddings():
    """
    Manually trigger an update of the vector embeddings
    
    Useful when you've added alumni through other means and want to
    ensure the search index is up to date.
    """
    try:
        logger.info("Manually triggering embeddings update...")
        success = rag_service.update_vectorstore()
        
        if success:
            return {"message": "Embeddings updated successfully"}
        else:
            return {"message": "No updates were needed"}
            
    except Exception as e:
        logger.error(f"Error updating embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Check the health status of all services
    """
    try:
        health = rag_service.health_check()
        
        status = "healthy" if all(
            service == "healthy" for service in [health["mongodb"], health["vectorstore"]]
        ) else "unhealthy"
        
        return HealthCheckResponse(
            status=status,
            **health
        )
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    API root endpoint with basic information
    """
    return {
        "message": "Alumni RAG API",
        "version": "1.0.0",
        "description": "AI-powered question answering for Alumni Management System",
        "endpoints": {
            "query": "POST /query - Ask questions about alumni",
            "add_alumni": "POST /alumni - Add new alumni",
            "conversation_history": "GET /conversation/{session_id} - Get chat history",
            "clear_conversation": "DELETE /conversation/{session_id} - Clear chat history",
            "update_embeddings": "POST /update-embeddings - Force update search index",
            "health": "GET /health - Check service health",
            "docs": "GET /docs - Interactive API documentation"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Set to False in production
        log_level="info"
    )