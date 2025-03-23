from typing import Literal

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    JWT_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()