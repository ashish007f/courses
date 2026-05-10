from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Core Banking Simulator"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    # Topic Names
    TOPIC_CUSTOMERS: str = "customers"
    TOPIC_ACCOUNTS: str = "accounts"
    TOPIC_TRANSACTIONS: str = "transactions"
    TOPIC_BALANCES: str = "balances"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
