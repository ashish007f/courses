from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class IngestionSettings(BaseSettings):
    # Spark Configuration
    spark_master: str = "local[*]"
    spark_app_name: str = "UnifiedBronzeIngestion"

    # MinIO Configuration
    minio_endpoint: str = "http://localhost:9000"
    minio_access_key: str = "admin"
    minio_secret_key: str = "password"

    # Kafka Configuration
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topics: List[str] = ["customers", "accounts", "transactions", "balances"]

    # Bronze Paths
    bronze_base_path: str = "s3a://bronze"
    checkpoint_base_path: str = "s3a://bronze/_checkpoints"

    # Batch Landing Zone
    batch_landing_zone: str = "vol/batch_landing"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = IngestionSettings()
