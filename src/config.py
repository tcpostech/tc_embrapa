"""
Configuration class responsible for getting all env parameters of the application
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration class responsible for getting all env parameters of the application"""
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    DOMAIN_URL: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


Config = Settings()
