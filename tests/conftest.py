import pytest

from sqlalchemy import NullPool, delete, event, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from httpx import ASGITransport, AsyncClient

from app.db.base import Base
from app.db.models import PullRequest, PullRequestReviewer, Team, User
from app.db.session import create_async_session
from app.main import app


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@localhost:5434/test_db",
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="session")
async def async_session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def db_session(async_session_maker):
    async with async_session_maker() as session:
        
        yield session
        
        await session.execute(
            text("TRUNCATE TABLE teams, users, pull_requests, pull_request_reviewers RESTART IDENTITY CASCADE;")
        )
        await session.commit()


@pytest.fixture
async def async_client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[create_async_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()
