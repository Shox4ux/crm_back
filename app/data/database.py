from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import os
from dotenv import load_dotenv

load_dotenv(os.getenv("ENV_FILE"))

print("ENV_FILE =", os.getenv("ENV_FILE"))
print("ASYNC_DATABASE_URL =", os.getenv("ASYNC_DATABASE_URL"))
print("SYNC_DATABASE_URL =", os.getenv("SYNC_DATABASE_URL"))

ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

local_url = "postgresql+asyncpg://postgres:1@localhost:5432/th_test"

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    # local_url,
    # "postgresql+asyncpg://myuser:mypassword@db:5433/mydb",
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False, bind=engine, class_=AsyncSession
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
