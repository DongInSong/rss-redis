import json
import redis.asyncio as redis
from app.config import settings

class CacheRepository:
    def __init__(self, r: redis.Redis):
        self._redis = r

    async def get_news(self, query: str) -> str | None:
        return await self._redis.get(f"rss:{query}")

    async def set_news(self, query: str, data: list[dict]):
        await self._redis.setex(f"rss:{query}", settings.CACHE_TTL, json.dumps(data))

    async def increment_hits(self):
        await self._redis.incr("stats:hit")

    async def increment_misses(self):
        await self._redis.incr("stats:miss")

    async def get_stats(self) -> dict[str, int]:
        hit = await self._redis.get("stats:hit")
        miss = await self._redis.get("stats:miss")
        return {"hit": int(hit or 0), "miss": int(miss or 0)}

    async def get_all_keys(self) -> list[str]:
        return await self._redis.keys("rss:*")

    async def get_all_cached_data(self) -> dict:
        cached_data = {}
        keys = await self.get_all_keys()
        for key in sorted(keys):
            val = await self._redis.get(key)
            try:
                cached_data[key] = json.loads(val)
            except (json.JSONDecodeError, TypeError):
                cached_data[key] = f"Error decoding JSON for key: {key}"
        return cached_data

    async def delete_by_query(self, query: str) -> int:
        return await self._redis.delete(f"rss:{query}")

    async def delete_all(self) -> int:
        keys = await self.get_all_keys()
        if not keys:
            return 0
        return await self._redis.delete(*keys)
