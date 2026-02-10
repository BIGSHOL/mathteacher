import os
import json
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings."""

    # Database - 환경변수 필수 (프로덕션에서는 기본값 없음)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mathtest" if os.getenv("ENV", "development") == "development" else "")

    # JWT - 환경변수 필수 (프로덕션에서는 기본값 없음)
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-only-secret-key-change-in-production" if os.getenv("ENV", "development") == "development" else "")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

    # Environment
    ENV: str = "development"  # development, staging, production

    # Gemini AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash"

    # CORS - 환경변수에서 JSON 배열 파싱
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # 쉼표로 구분된 문자열도 허용
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @field_validator("JWT_SECRET")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if not v or v == "":
            raise ValueError("JWT_SECRET must be set via environment variable in production")
        if len(v) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v or v == "":
            raise ValueError("DATABASE_URL must be set via environment variable in production")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
