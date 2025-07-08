import feedparser

RSS_FEEDS = [
    "https://rss.etnews.com/Section902.xml",
    "https://www.yna.co.kr/rss/politics.xml",
    "https://news.google.com/rss/search?q={query}",
]

def fetch_rss(query: str):
    result = []
    for url in RSS_FEEDS:
        final_url = url.format(query=query)
        feed = feedparser.parse(final_url)
        for entry in feed.entries:
            if query.lower() in entry.title.lower() or query.lower() in entry.summary.lower():
                result.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.summary,
                    "published": entry.get("published", ""),
                    "source": feed.feed.get("title", "")
                })
    return result
