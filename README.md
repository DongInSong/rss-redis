# RSS News Feed Caching with Redis

![License](https://img.shields.io/github/license/DongInSong/rss-redis)
![Last Commit](https://img.shields.io/github/last-commit/DongInSong/rss-redis)

## 1. Overview

FastAPI와 Redis를 활용해 RSS 뉴스 검색 결과를 캐싱하고, 계층별 책임 분리를 적용한 경량 웹 API 프로젝트입니다.

A lightweight web API project using FastAPI and Redis to cache RSS news search results with clear separation of concerns across application layers.

## 2. Features

- **Keyword-based News Search**: Fetches real-time news from multiple RSS feeds based on user-provided keywords.
- **Redis Caching**: Search results are cached in Redis for a specified Time-To-Live (TTL), ensuring rapid responses for repeated requests.
- **Cache Statistics**: Tracks the number of cache hits and misses to monitor cache efficiency.
- **Performance Testing**: Includes a script to compare performance with and without the cache.

## 3. Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 4. Architecture

- **Routers**: Defines API endpoints and forwards client requests to the service layer.
- **Services**: Handles the core business logic, including checking the cache, fetching external RSS feeds, and processing data.
- **Repositories**: Manages interactions with the database (Redis), encapsulating data query, storage, and deletion logic.
- **Schemas**: Uses Pydantic models to define the structure and validation for API request and response data.

## 5. Project Structure

```
.
├── app
│   ├── core              # Core application settings (Redis, logging, exception handling)
│   ├── repositories      # Data persistence management (Redis interaction)
│   ├── routers           # API endpoint definitions
│   ├── schemas           # Pydantic data models (schemas)
│   ├── services          # Business logic processing
│   ├── config.py         # Environment variables and configuration management
│   └── main.py           # FastAPI application entry point
├── tests
│   └── performance_test.py # Performance testing script
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker image build configuration
└── requirements.txt      # Python dependency list
```

## 6. Installation & Execution

### Using Docker Compose (Recommended)

In the project root directory, run the following command to start the FastAPI application and Redis server simultaneously:

```bash
docker compose up --build
```

The application will be available at `http://localhost:8000`.

### Manual Setup

- Python 3.8+
- A running Redis server

1.  **Clone the repository**
    ```bash
    git clone https://github.com/DongInSong/rss-redis.git
    cd rss-redis
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Redis server (via docker)**
    ```bash
    docker run --name redis -p 6379:6379 -d redis
    ```

4.  **Start the API server**
    ```bash
    uvicorn app.main:app --reload
    ```

## 7. API Endpoints

- `GET /rss/search?q={keyword}`: Searches for news by keyword. Returns cached data if available; otherwise, fetches new data from RSS feeds, caches it, and then returns it.
- `GET /rss/metrics`: Returns the number of cache hits and misses.
- `GET /rss/keys`: Returns a list of all `rss:*` keys stored in Redis.
- `GET /rss/cache`: Returns all cached `rss:*` data.
- `DELETE /rss/cache`: Deletes all cached data.
- `DELETE /rss/cache/{keyword}`: Deletes cached data for a specific keyword.

**cURL Examples:**
```bash
# Search for news with the keyword "AI"
curl "http://127.0.0.1:8000/rss/search?q=ai"

# Get all cache keys
curl "http://127.0.0.1:8000/rss/keys"

# Delete all cache
curl -X DELETE "http://127.0.0.1:8000/rss/cache"
```

## 8. Performance Testing

The `tests/performance_test.py` script compares the performance between fetching from the cache and fetching directly from RSS feeds.

**Command:**
```bash
python -m tests.performance_test [keyword]
```
- `[keyword]`: The keyword to use for the test (defaults to `fastapi`).

**Test Steps:**
1.  Clear all existing cache data.
2.  Measure the response time for fetching data directly from external RSS feeds.
3.  Save the fetched data to Redis.
4.  Measure the response time for fetching the same data from the Redis cache and compare the results to evaluate performance gains.

## 9. Project Goals & Achievements

- This project was developed as a client application to test the functionality and performance of a custom-built `mini-redis` server.
- The `mini-redis` project, a C++-based Redis clone, has been successfully validated for compatibility with standard Redis clients (`redis-py`) through this application.
- **Key Achievements:**
  - Verified the stability and real-world performance of the `mini-redis` server.
  - Confirmed seamless integration with a standard Python Redis library.

[![GitHub](https://img.shields.io/badge/mini_redis-181717?style=flat&logo=github&logoColor=white)](https://github.com/DongInSong/mini-redis)
