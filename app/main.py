from fastapi import FastAPI, HTTPException
from app.routers import rss_cache_router as redis_router
from app.core.exception_handler import *
import redis.exceptions

app = FastAPI()

register_exception_handlers(app)

app.include_router(redis_router)

@app.get("/")
def root():
    return {"message": "Welcome to the RSS News Search API. Use /search?q=<query> to search for news."}
