from fastapi import FastAPI, HTTPException, Query
from app.rss_reader import fetch_rss
from .redis_client import delete_all_cache, delete_cache_by_query, get_all_keys, get_cached_news, set_cached_news, incr_hit, incr_miss, get_stats, get_all_cached
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

@app.get("/keys")
def get_keys():
    return get_all_keys()

@app.get("/cache")
def get_cache():
    return get_all_cached()

@app.delete("/cache/{query}")
def delete_cache(query: str):  
    code = delete_cache_by_query(query)
    if not code:
        raise HTTPException(status_code=404, detail="Cache not found")
    return {"message": f"Cache for query '{query}' deleted successfully."}

@app.delete("/cache")
def delete_all():
    count = delete_all_cache()
    if count == 0:
        raise HTTPException(status_code=404, detail="No cache found to delete")
    return {"message": f"All caches deleted successfully. {count} items removed."}  