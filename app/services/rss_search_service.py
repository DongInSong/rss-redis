import json
from loguru import logger
from app.repositories.cache_repository import CacheRepository
from app.services.rss_service import fetch_rss

class RssSearchService:
    def __init__(self, cache_repo: CacheRepository):
        self._cache_repo = cache_repo

    async def search(self, query: str) -> dict:
        try:
            cached_news_str = await self._cache_repo.get_news(query)
        
            if cached_news_str:
                await self._cache_repo.increment_hits()
                news_data = json.loads(cached_news_str)
                return {"items": news_data}

            await self._cache_repo.increment_misses()
            news_data = await fetch_rss(query)
        
            if news_data:
                await self._cache_repo.set_news(query, news_data)
            
            return {"items": news_data}
        except Exception as e:
            logger.exception(f"Error during RSS search for '{query}': {str(e)}")
            raise
