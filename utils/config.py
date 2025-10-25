from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEMO_MODE: bool = True
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
