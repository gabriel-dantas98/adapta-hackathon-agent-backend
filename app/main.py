"""
Main FastAPI application.
"""
import asyncio
import logging
import traceback
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import uvicorn

from app.core.config import settings
from app.core.database import database_manager
from app.core.embeddings import embedding_service
from app.schemas.common import HealthResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up application...")
    
    try:
        # Initialize database
        await database_manager.initialize()
        logger.info("Database initialized successfully")
        
        # Initialize embedding service
        health_check = await embedding_service.health_check()
        if health_check["status"] == "healthy":
            logger.info("Embedding service initialized successfully")
        else:
            logger.error(f"Embedding service health check failed: {health_check}")
            
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        logger.warning("Continuing without database connection...")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    
    try:
        # Close database connections
        await database_manager.close()
        logger.info("Database connections closed")
        
    except Exception as e:
        logger.error(f"Shutdown error: {str(e)}")

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered backend for hackathon agent with vector similarity search",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts,
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = asyncio.get_event_loop().time()
    
    # Log request
    logger.info(f"{request.method} {request.url.path} - {request.client.host}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = asyncio.get_event_loop().time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation error",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "errors": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {str(exc)}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "error": str(exc) if settings.debug else "Internal server error"
        }
    )

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check database
        try:
            db_health = await database_manager.health_check()
        except Exception as e:
            db_health = {"status": "unavailable", "error": str(e)}
        
        # Check embedding service
        try:
            embedding_health = await embedding_service.health_check()
        except Exception as e:
            embedding_health = {"status": "unavailable", "error": str(e)}
        
        # Overall status
        is_healthy = (
            db_health.get("status") == "healthy" and
            embedding_health.get("status") == "healthy"
        )
        
        services = {
            "database": db_health.get("status", "unknown"),
            "embedding_service": embedding_health.get("status", "unknown"),
        }
        
        return HealthResponse(
            status="healthy" if is_healthy else "degraded",
            services=services,
            version=settings.app_version
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            services={"error": str(e)},
            version=settings.app_version
        )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Adapta Hackathon Agent Backend",
        "version": settings.app_version,
        "docs_url": "/docs" if settings.debug else None
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info"
    ) 
