import pytest

from sqlalchemy import NullPool, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from httpx import ASGITransport, AsyncClient

from app.db.base import Base
from app.db.session import create_async_session
from app.main import app


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@localhost:5434/test_db",
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all())
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all())
    
    await engine.dispose()


@pytest.fixture(scope="session")
async def async_session_maker(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def db_session(engine, async_session_maker):
    async with engine.connect() as conn:
        trans = await conn.begin()

        async with async_session_maker(bind=conn) as session:
            await session.begin_nested() # savepoint (вложенная транзакция), чтобы при commit основная осталась жива

            # если в коде ошибка и вызовется rollback, пересоздаем savepoint
            @event.listens_for(session.sync_session, "after_transaction_end")
            def end_savepoint(session, trans):
                if not session._nested_transaction:
                    if session.is_active:
                        session.begin_nested()

            yield session

            if trans.is_active:
                await trans.rollback()


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
