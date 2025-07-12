from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    CACHE_TTL: int = 60 * 5  # 5분 TTL

    RSS_FEEDS: list[str] = [
        "https://news.google.com/rss/search?q={query}",
        "https://www.bing.com/news/search?q={query}&format=rss",
        "https://news.yahoo.com/rss?p={query}",
    ]

settings = Settings()
