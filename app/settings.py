from pydantic_settings import BaseSettings


# POSTGRES_USER=c_user
# POSTGRES_PASSWORD=1234
# POSTGRES_DB=crmdb


# # For Alembic migrations
# SYNC_DATABASE_URL="postgresql+psycopg2://postgres:1@localhost:5432/crm_db"

# # For async SQLAlchemy engine
# ASYNC_DATABASE_URL="postgresql+asyncpg://postgres:1@localhost:5432/crm_db"


# ALGORITHM = "HS256"
# EXPIRES = 60  # 1 hour
# TOKEN_KEY = "2689561ae8fb07c9fa1fb39a92a9a6d89dc930a5085da14507a43f53a8ab47b8"


class Settings(BaseSettings):
    ALGORITHM: str
    ASYNC_DATABASE_URL: str
    SYNC_DATABASE_URL: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    ASSETS_FOLDER_PATH: str

    TOKEN_KEY: str
    EXPIRES: int = 60

    class Config:
        env_file = ".env"
