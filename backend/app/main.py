import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.db.base import Base
import app.models
from app.db.session import engine, SessionLocal
from app.api.auth import router as auth_router
from app.api.complaints import router as complaints_router
from app.api.policies import router as policies_router
from app.api.audit import router as audit_router
from app.services.rag import rag_engine

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    logger.info("Initializing CivicResolve Guardian database schema...")
    Base.metadata.create_all(bind=engine)
    
    # Auto-index policy charters into RAG database
    db = SessionLocal()
    try:
        rag_engine.index_markdown_policies(db)
    finally:
        db.close()
        
    logger.info("CivicResolve Guardian startup complete.")
    yield
    logger.info("CivicResolve Guardian shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multilingual, Evidence-Grounded Public Grievance Triage, Routing and Resolution Quality Platform",
    lifespan=lifespan
)

# CORS Middleware with explicit origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"]
)

# Request ID & Audit Timing Middleware
@app.middleware("http")
async def request_id_and_audit_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    
    # Security Headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response

# Global Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. This transaction has been safely logged."
        }
    )

# Health & Version endpoints
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time()
    }

@app.get("/version", tags=["System"])
def version_check():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "api_version": settings.API_V1_STR
    }

# Include API v1 Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(complaints_router, prefix=settings.API_V1_STR)
app.include_router(policies_router, prefix=settings.API_V1_STR)
app.include_router(audit_router, prefix=settings.API_V1_STR)
