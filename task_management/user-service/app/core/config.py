
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: str

    # admin account
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    KAFKA_BOOTSTRAP_SERVERS: str
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
