from fastapi import APIRouter, HTTPException, Query, Depends
import redis.asyncio as redis

from app.core.redis import get_redis_client
from app.repositories.cache_repository import CacheRepository
from app.services.rss_search_service import RssSearchService
from app.schemas.rss_schema import RSSFeed

router = APIRouter(
    prefix="/rss",
    tags=["RSS Cache"],
    responses={404: {"description": "Not found"}}
)

# Dependency Providers
def get_cache_repository(r: redis.Redis = Depends(get_redis_client)) -> CacheRepository:
    return CacheRepository(r)

def get_rss_search_service(repo: CacheRepository = Depends(get_cache_repository)) -> RssSearchService:
    return RssSearchService(repo)

# Routes
@router.get("/ping")
async def ping(r: redis.Redis = Depends(get_redis_client)):
    return await r.ping()

@router.get("/search", response_model=RSSFeed)
async def search_news(
    q: str = Query(..., min_length=1),
    service: RssSearchService = Depends(get_rss_search_service)
):
    return await service.search(q)

@router.get("/metrics")
async def metrics(repo: CacheRepository = Depends(get_cache_repository)):
    return await repo.get_stats()

@router.get("/keys")
async def get_keys(repo: CacheRepository = Depends(get_cache_repository)):
    return await repo.get_all_keys()

@router.get("/cache")
async def get_cache(repo: CacheRepository = Depends(get_cache_repository)):
    return await repo.get_all_cached_data()

@router.delete("/cache/{query}")
async def delete_cache(
    query: str,
    repo: CacheRepository = Depends(get_cache_repository)
):  
    deleted_count = await repo.delete_by_query(query)
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Cache not found")
    return {"message": f"Cache for query '{query}' deleted successfully."}

@router.delete("/cache")
async def delete_all(repo: CacheRepository = Depends(get_cache_repository)):
    count = await repo.delete_all()
    if count == 0:
        raise HTTPException(status_code=404, detail="No cache found to delete")
    return {"message": f"All caches deleted successfully. {count} items removed."}
