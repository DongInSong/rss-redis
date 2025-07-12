from fastapi import APIRouter, HTTPException, Query, Depends
from app.services.rss_service import fetch_rss
from app.core.redis import get_redis_client
import redis.asyncio as redis
import json

router = APIRouter(
    prefix="/rss",
    tags=["RSS Cache"],
    responses={404: {"description": "Not found"}}
)

@router.get("/ping")
async def ping(r: redis.Redis = Depends(get_redis_client)):
    return await r.ping()

@router.get("/search")
async def search_news(q: str = Query(..., min_length=1), r: redis.Redis = Depends(get_redis_client)):
    cached = await r.get(f"rss:{q}")
    if cached:
        await r.incr("stats:hit")
        return {"source": "cache", "data": json.loads(cached)}
    
    await r.incr("stats:miss")
    news = await fetch_rss(q)
    await r.setex(f"rss:{q}", 60 * 5, json.dumps(news))
    return {"source": "rss", "data": news}

@router.get("/metrics")
async def metrics(r: redis.Redis = Depends(get_redis_client)):
    hit = await r.get("stats:hit")
    miss = await r.get("stats:miss")
    return {
        "hit": int(hit or 0),
        "miss": int(miss or 0)
    }

@router.get("/keys")
async def get_keys(r: redis.Redis = Depends(get_redis_client)):
    return await r.keys("rss:*")

@router.get("/cache")
async def get_cache(r: redis.Redis = Depends(get_redis_client)):
    cached_data = {}
    keys = await r.keys("rss:*")
    for key in sorted(keys):
        val = await r.get(key)
        try:
            cached_data[key] = json.loads(val)
        except (json.JSONDecodeError, TypeError):
            cached_data[key] = f"Error decoding JSON for key: {key}"
    return cached_data

@router.delete("/cache/{query}")
async def delete_cache(query: str, r: redis.Redis = Depends(get_redis_client)):  
    deleted_count = await r.delete(f"rss:{query}")
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Cache not found")
    return {"message": f"Cache for query '{query}' deleted successfully."}

@router.delete("/cache")
async def delete_all(r: redis.Redis = Depends(get_redis_client)):
    keys = await r.keys("rss:*")
    if keys:
        deleted_count = await r.delete(*keys)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="No cache found to delete")
        return {"message": f"All caches deleted successfully. {deleted_count} items removed."}
    raise HTTPException(status_code=404, detail="No cache found to delete")
