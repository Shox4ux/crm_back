import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.data.database import get_db
from app.data.base import Base

# Ensure this matches your test database credentials
DATABASE_URL = "postgresql+asyncpg://postgres:1@localhost/testdb"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    """
    Create a single engine for the whole session.
    StaticPool is used to maintain a single connection that persists
    across different requests within the same test.
    """
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        # Start fresh: drop and recreate tables
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(engine):
    """
    Provides a database session that stays alive for the duration of a single test.
    We commit after each action to ensure visibility across HTTP calls.
    """
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        yield session
        # Rollback after the test is complete to keep tests isolated
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session):
    """
    Creates an AsyncClient for FastAPI that uses the overridden db_session.
    """

    async def _get_test_db():
        try:
            yield db_session
        finally:
            # We don't close here because the fixture handles cleanup
            pass

    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    # Clean up overrides after each test function
    app.dependency_overrides.clear()
