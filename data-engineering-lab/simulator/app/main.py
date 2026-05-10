from fastapi import FastAPI
from .core.config import settings
from .core.database import init_db
from .api.customer_routes import router as customer_router
from .api.banking_routes import router as banking_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Database Tables
    await init_db()
    yield
    # Shutdown logic if needed

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.include_router(customer_router)
app.include_router(banking_router)
