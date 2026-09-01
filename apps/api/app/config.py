from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "finance_controller"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/finance_controller"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4jpassword"
    
    # Temporal
    TEMPORAL_URL: str = "localhost:7233"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # Razorpay
    RAZORPAY_MODE: str = "test"  # 'test' or 'live'
    
    RAZORPAY_TEST_KEY_ID: Optional[str] = None
    RAZORPAY_TEST_KEY_SECRET: Optional[str] = None
    
    RAZORPAY_LIVE_KEY_ID: Optional[str] = None
    RAZORPAY_LIVE_KEY_SECRET: Optional[str] = None
    
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def razorpay_key_id(self) -> Optional[str]:
        return self.RAZORPAY_LIVE_KEY_ID if self.RAZORPAY_MODE == "live" else self.RAZORPAY_TEST_KEY_ID
        
    @property
    def razorpay_key_secret(self) -> Optional[str]:
        return self.RAZORPAY_LIVE_KEY_SECRET if self.RAZORPAY_MODE == "live" else self.RAZORPAY_TEST_KEY_SECRET

settings = Settings()
