import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL = 60 * 5  # 5분 TTL

RSS_FEEDS = [
    "https://news.google.com/rss/search?q={query}",
    "https://www.bing.com/news/search?q={query}&format=rss",
    "https://news.yahoo.com/rss?p={query}",
]

__all__ = ["REDIS_HOST", "REDIS_PORT", "CACHE_TTL", "RSS_FEEDS"]
