import redis
import json
from .config import REDIS_HOST, REDIS_PORT, CACHE_TTL

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_cached_news(query: str):
    return r.get(f"rss:{query}")

def set_cached_news(query: str, data):
    r.setex(f"rss:{query}", CACHE_TTL, json.dumps(data))

def incr_hit():
    r.incr("stats:hit")

def incr_miss():
    r.incr("stats:miss")

def get_stats():
    return {
        "hit": int(r.get("stats:hit") or 0),
        "miss": int(r.get("stats:miss") or 0)
    }
