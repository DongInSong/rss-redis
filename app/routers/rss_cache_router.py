from fastapi import APIRouter, HTTPException, Query
from app.services.rss_service import fetch_rss
from app.core.redis import *
import json

router = APIRouter(
    prefix="/rss",
    tags=["RSS Cache"],
    responses={404: {"description": "Not found"}}
)

@router.get("/ping")
async def ping():
    return await get_ping()

@router.get("/search")
async def search_news(q: str = Query(..., min_length=1)):
    cached = await get_cached_news(q)
    if cached:
        await incr_hit()
        return {"source": "cache", "data": json.loads(cached)}
    
    await incr_miss()
    news = await fetch_rss(q)
    await set_cached_news(q, news)
    return {"source": "rss", "data": news}

@router.get("/metrics")
async def metrics():
    return await get_stats()

@router.get("/keys")
async def get_keys():
    return await get_all_keys()

@router.get("/cache")
async def get_cache():
    return await get_all_cached()

@router.delete("/cache/{query}")
async def delete_cache(query: str):  
    code = await delete_cache_by_query(query)
    if not code:
        raise HTTPException(status_code=404, detail="Cache not found")
    return {"message": f"Cache for query '{query}' deleted successfully."}

@router.delete("/cache")
async def delete_all():
    count = await delete_all_cache()
    if count == 0:
        raise HTTPException(status_code=404, detail="No cache found to delete")
    return {"message": f"All caches deleted successfully. {count} items removed."}
