from fastapi import FastAPI
from app.router import redis as redis_router

app = FastAPI()

app.include_router(redis_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to the RSS News Search API. Use /search?q=<query> to search for news."}
