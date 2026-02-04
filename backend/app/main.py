from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .core.config import settings
from .core.logger import logger
from .core.database import engine
from .models import db_models
from .routers import chat

# Create tables
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sarvam Multilingual Chat API",
    description="Professional Enterprise-Grade API for Multilingual Agriculture Chatbot",
    version="1.0.0"
)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event
@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")

# Routes
app.include_router(chat.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
