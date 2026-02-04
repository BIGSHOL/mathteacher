from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def _get_async_url(url: str) -> str:
    """Convert sync DB URL to async driver URL."""
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
    return url


# Async engine (runtime)
_async_url = _get_async_url(settings.DATABASE_URL)
_async_kwargs: dict = {}
if _async_url.startswith("sqlite"):
    _async_kwargs["connect_args"] = {"check_same_thread": False}

async_engine = create_async_engine(_async_url, **_async_kwargs)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Sync engine (for init_db / create_all / Alembic)
if settings.DATABASE_URL.startswith("sqlite"):
    sync_engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    sync_engine = create_engine(settings.DATABASE_URL)


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


async def get_db():
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        yield session
