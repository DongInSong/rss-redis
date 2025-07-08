import feedparser

RSS_FEEDS = [
    "https://news.google.com/rss/search?q={query}",
    "https://www.bing.com/news/search?q={query}&format=rss",
    "https://news.yahoo.com/rss?p={query}",
]

def fetch_rss(query: str):
    result = []
    for url in RSS_FEEDS:
        final_url = url.format(query=query)
        feed = feedparser.parse(final_url)
        for entry in feed.entries:
            if query.lower() in entry.title.lower():
            # or query.lower() in entry.summary.lower():
                result.append({
                    "title": entry.title,
                    "link": entry.link,
                    # "summary": entry.summary,
                    # "published": entry.get("published", ""),
                    # "source": feed.feed.get("title", "")
                })
    return result
