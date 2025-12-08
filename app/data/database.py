from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.settings import Settings

settings = Settings()

engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False, bind=engine, class_=AsyncSession
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
