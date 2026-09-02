from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.core import Customer, Invoice, Payment, Settlement, RouteTransfer
from app.config import settings
import sentry_sdk
from prometheus_client import make_asgi_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    logger.info("Sentry SDK initialized.")

app = FastAPI(
    title="AI Finance Controller API",
    description="Graph-powered finance-operations platform API",
    version="1.0.0"
)

# Add Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For hackathon simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
