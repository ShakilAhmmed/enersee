from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import Field
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )

    # Database
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str = Field(..., alias="DB_USERNAME")
    DB_PASSWORD: str
    DB_NAME: str = Field(..., alias="DB_DATABASE")
    EXTERNAL_API_BASE: str = Field(..., alias="EXTERNAL_API_BASE")
    EXTERNAL_API_KEY: str = Field(..., alias="EXTERNAL_API_KEY")

    # Application
    APP_NAME: str = "Enersee Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api"

    @property
    def DATABASE_URL(self) -> str:
        # print(f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
