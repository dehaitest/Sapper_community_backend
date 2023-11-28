from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    WEBSOCKET_ROUTE: str
    API_V1_STR: str
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_MODEL: str
    OPENAI_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
