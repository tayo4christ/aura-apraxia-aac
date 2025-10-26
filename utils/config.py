from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # existing
    DEMO_MODE: bool = True
    LOG_LEVEL: str = "INFO"

    # new (safe defaults; can be overridden via .env or environment)
    APP_NAME: str = "AURA Apraxia Therapy"
    MODEL_PATH: str = "speech_recognition/models/wav2vec2"
    # "auto" = pick CUDA if available, else CPU (handled in the app)
    DEVICE: str = "auto"

    class Config:
        env_file = ".env"


settings = Settings()
