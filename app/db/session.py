from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

engine = create_async_engine(settings.database_url)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_async_session():
    async with async_session_maker() as session:
        yield session


session_db = Annotated[AsyncSession, Depends(create_async_session)]
