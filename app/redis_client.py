import redis
import json
from .config import REDIS_HOST, REDIS_PORT, CACHE_TTL

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_cached_news(query: str):
    return r.get(f"rss:{query}")

def set_cached_news(query: str, data):
    r.setex(f"rss:{query}", CACHE_TTL, json.dumps(data))
    
def delete_cache_by_query(query: str) -> bool:
    return r.delete(f"rss:{query}") > 0

def delete_all_cache()  -> int:
    keys = r.keys("rss:*")
    if keys:
        r.delete(*keys)
        return len(keys)
    return False

def incr_hit():
    r.incr("stats:hit")

def incr_miss():
    r.incr("stats:miss")

def get_stats():
    return {
        "hit": int(r.get("stats:hit") or 0),
        "miss": int(r.get("stats:miss") or 0)
    }

def get_all_keys():
    return r.keys("rss:*")

def get_all_cached():
    cached_data = {}
    for key in sorted(r.keys("rss:*")):
        val = r.get(key)
        try:
            cached_data[key] = json.loads(val)
        except (json.JSONDecodeError, TypeError):
            cached_data[key] = f"Error decoding JSON for key: {key}"
    return cached_data
