from __future__ import annotations
import os

class Settings:
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
    S3_BUCKET_RAW: str = os.getenv("S3_BUCKET_RAW", "eda-raw")
    S3_BUCKET_PROFILES: str = os.getenv("S3_BUCKET_PROFILES", "eda-profiles")
    S3_BUCKET_ARTIFACTS: str = os.getenv("S3_BUCKET_ARTIFACTS", "eda-artifacts")
    S3_BUCKET_OUTPUTS: str = os.getenv("S3_BUCKET_OUTPUTS", "eda-outputs")

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "storyteller")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "storyteller")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "storyteller")

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")

settings = Settings()