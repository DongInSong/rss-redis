import redis.asyncio as redis
import json
from app.config import REDIS_HOST, REDIS_PORT, CACHE_TTL

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def incr_hit():
    await r.incr("stats:hit")

async def incr_miss():
    await r.incr("stats:miss")

async def get_ping():
    return await r.ping()

async def set_cached_news(query: str, data):
    await r.setex(f"rss:{query}", CACHE_TTL, json.dumps(data))
    
async def get_cached_news(query: str):
    return await r.get(f"rss:{query}")

async def get_stats():
    hit = await r.get("stats:hit")
    miss = await r.get("stats:miss")
    return {
        "hit": int(hit or 0),
        "miss": int(miss or 0)
    }

async def get_all_keys():
    return await r.keys("rss:*")

async def get_all_cached():
    cached_data = {}
    keys = await r.keys("rss:*")
    for key in sorted(keys):
        val = await r.get(key)
        try:
            cached_data[key] = json.loads(val)
        except (json.JSONDecodeError, TypeError):
            cached_data[key] = f"Error decoding JSON for key: {key}"
    return cached_data

async def delete_cache_by_query(query: str) -> bool:
    deleted_count = await r.delete(f"rss:{query}")
    return deleted_count > 0

async def delete_all_cache() -> int:
    keys = await r.keys("rss:*")
    if keys:
        deleted_count = await r.delete(*keys)
        return deleted_count
    return 0
