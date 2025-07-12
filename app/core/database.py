"""
Database configuration and session management.
"""
import asyncio
from typing import AsyncGenerator, Optional, Dict, Any
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings


# Create async engine
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=StaticPool,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create sync engine for migrations (convert async URL to sync)
sync_database_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
sync_engine = create_engine(
    sync_database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create sessionmakers
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async database session dependency.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_db():
    """
    Sync database session for migrations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """
    Initialize database tables.
    """
    async with async_engine.begin() as conn:
        # Enable pgvector extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close database connections.
    """
    await async_engine.dispose()
    sync_engine.dispose()


# Health check function
async def check_db_health() -> bool:
    """
    Check database connection health.
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception:
        return False


class DatabaseManager:
    """Database manager for handling database operations."""
    
    def __init__(self):
        self.async_engine = async_engine
        self.sync_engine = sync_engine
        self.async_session = AsyncSessionLocal
        self.sync_session = SessionLocal
    
    async def initialize(self):
        """Initialize database."""
        await init_db()
    
    async def close(self):
        """Close database connections."""
        await close_db()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database health."""
        try:
            is_healthy = await check_db_health()
            return {
                "status": "healthy" if is_healthy else "unhealthy",
                "database_url": settings.database_url
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


# Global database manager instance
database_manager = DatabaseManager() 
