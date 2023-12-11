# app/services/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..core.config import settings  # Import your settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db_session():
    async with SessionLocal() as session:
        yield session
