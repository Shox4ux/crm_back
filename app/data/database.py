from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import Settings

settings = Settings()


engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=True,
    #     Why needed?
    # `pool_pre_ping=True` → tests connections before use, avoids “closed connection”
    # `pool_recycle` → refreshes pool connections to avoid stale/timeout disconnects
    pool_pre_ping=True,
    pool_recycle=300,
)

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
