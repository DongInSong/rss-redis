from fastapi import FastAPI, Query
from .rss_reader import fetch_rss
from .redis_client import get_cached_news, set_cached_news, incr_hit, incr_miss, get_stats
import json

app = FastAPI()

@app.get("/search")
def search_news(q: str = Query(..., min_length=1)):
    cached = get_cached_news(q)
    if cached:
        incr_hit()
        return {"source": "cache", "data": json.loads(cached)}
    
    incr_miss()
    news = fetch_rss(q)
    set_cached_news(q, news)
    return {"source": "rss", "data": news}

@app.get("/metrics")
def metrics():
    return get_stats()
