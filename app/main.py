from fastapi import FastAPI
from app.routers import rss_cache_router as redis_router
from app.core.exception_handler import *
import redis.exceptions

app = FastAPI()

app.add_exception_handler(redis.exceptions.ConnectionError, redis_connection_error_handler)
app.add_exception_handler(redis.exceptions.ResponseError, redis_response_error_handler)

app.include_router(redis_router)

@app.get("/")
def root():
    return {"message": "Welcome to the RSS News Search API. Use /search?q=<query> to search for news."}
