from pydantic_settings import BaseSettings


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
        env_file = ".env.prod"
