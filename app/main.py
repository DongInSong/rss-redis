from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import rss_cache_router
from app.core.exception_handler import register_exception_handlers
from app.core.redis import redis_pool
from app.core.logging_config import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    yield
    # Shutdown
    await redis_pool.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(rss_cache_router)

register_exception_handlers(app)

@app.get("/")
def root():
    return {"message": "Welcome to the RSS News Search API. Use /search?q=<query> to search for news."}
