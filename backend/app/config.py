from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    MONGODB_URI: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
