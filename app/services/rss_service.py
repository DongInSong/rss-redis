import feedparser
import httpx
from app.config import RSS_FEEDS

async def fetch_rss(query: str):
    result = []
    async with httpx.AsyncClient() as client:
        for url in RSS_FEEDS:
            final_url = url.format(query=query)
            try:
                response = await client.get(final_url, timeout=5.0)
                response.raise_for_status()
                feed = feedparser.parse(response.text)
                for entry in feed.entries:
                    if query.lower() in entry.title.lower():
                        result.append({
                            "title": entry.title,
                            "link": entry.link,
                        })
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                print(f"Error fetching RSS feed from {final_url}: {e}")

    return result
