"""
Class responsible for application session
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import Config

engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=False))


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    This method is responsible for the postgres+asyncpg session.
    For more information see sessionmaker documentation.
    """
    session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with session() as session:
        yield session
