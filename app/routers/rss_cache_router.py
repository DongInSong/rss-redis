from fastapi import APIRouter, HTTPException, Query
from app.services import fetch_rss
from app.core.redis import *
import json

router = APIRouter(
    prefix="/rss",
    tags=["RSS Cache"],
    responses={404: {"description": "Not found"}}
)

@router.get("/ping")
def ping(m: str = Query(None, description="Optional message to echo back")):
    if m:
        return {m} 
    return {"PONG!"}

@router.get("/search")
def search_news(q: str = Query(..., min_length=1)):
    cached = get_cached_news(q)
    if cached:
        incr_hit()
        return {"source": "cache", "data": json.loads(cached)}
    
    incr_miss()
    news = fetch_rss(q)
    set_cached_news(q, news)
    return {"source": "rss", "data": news}

@router.get("/metrics")
def metrics():
    return get_stats()

@router.get("/keys")
def get_keys():
    return get_all_keys()

@router.get("/cache")
def get_cache():
    return get_all_cached()

@router.delete("/cache/{query}")
def delete_cache(query: str):  
    code = delete_cache_by_query(query)
    if not code:
        raise HTTPException(status_code=404, detail="Cache not found")
    return {"message": f"Cache for query '{query}' deleted successfully."}

@router.delete("/cache")
def delete_all():
    count = delete_all_cache()
    if count == 0:
        raise HTTPException(status_code=404, detail="No cache found to delete")
    return {"message": f"All caches deleted successfully. {count} items removed."}  