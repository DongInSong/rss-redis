import feedparser
import httpx
from loguru import logger
from app.config import settings

async def fetch_rss(query: str):
    result = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for url in settings.RSS_FEEDS:
            final_url = url.format(query=query)
            try:
                response = await client.get(final_url, timeout=5.0, headers=headers)
                response.raise_for_status()
                feed = feedparser.parse(response.text)
                for entry in feed.entries:
                    if query.lower() in entry.title.lower():
                        result.append({
                            "title": entry.title,
                            "link": entry.link,
                            "description": entry.get("summary", entry.get("description")),
                            "pubDate": entry.get("published", entry.get("pubDate")),
                        })
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                logger.error(f"Error fetching RSS feed from {final_url}: {e}")

    return result
