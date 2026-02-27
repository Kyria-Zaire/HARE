"""
HARE Pro v2.0 – Point d'entrée FastAPI.
CORS, security headers, rate limiting, routers v1.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.endpoints import admin, chatbot, newsletter, products, quiz
from app.core.config import get_settings
from app.core.limiter import limiter
from app.db.session import create_db_and_tables

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Démarrage : création des tables. Arrêt : cleanup si besoin."""
    create_db_and_tables()
    logger.info("HARE Pro API started", tables_created=True)
    yield
    logger.info("HARE Pro API shutting down")


app = FastAPI(
    title="HARE Pro API",
    description="Hair Analysis Recommendation Engine – Salon haut de gamme",
    version="2.0.0",
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """Health check pour Docker / load balancer."""
    return {"status": "ok", "version": "2.0.0"}


app.include_router(quiz.router, prefix=settings.api_v1_prefix)
app.include_router(products.router, prefix=settings.api_v1_prefix)
app.include_router(newsletter.router, prefix=settings.api_v1_prefix)
app.include_router(chatbot.router, prefix=settings.api_v1_prefix)
app.include_router(admin.router, prefix=settings.api_v1_prefix)


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response
