from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@localhost:5458/appdb"
    db_echo: bool = True


settings = Settings()
