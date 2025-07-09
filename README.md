# RSS News Feed Caching with Redis

## 1. Overview
FastAPI를 사용하여 특정 키워드에 대한 RSS 뉴스 피드를 파싱하고, Redis를 통해 검색 결과를 캐싱하여 응답 속도를 향상시키는 웹 서비스 기반 테스트 프로젝트입니다. API를 통해 실시간으로 뉴스를 검색하거나 캐시된 데이터를 빠르게 조회할 수 있습니다.   
This is a test project for a web service that parses RSS news feeds based on specific keywords using FastAPI and caches the search results with Redis to improve response speed. Users can fetch real-time news or quickly access previously cached data through API endpoints.

## 2. Features

- **Keyword-based News Search**: Search RSS feeds based on user-provided keywords.
- **Redis Caching**: Results are cached in Redis for a specified TTL (time to live), allowing faster responses for repeated requests.
- **Cache Statistics**: Tracks the number of cache hits and misses.
- **Data Retrieval**: Retrieve all cached keys or full cache data stored in Redis.
- **Performance Testing**: Includes test scripts to compare performance with and without cache.

## 3. Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)  ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)  ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)  


## 4. Installation & Execution

### Using Docker Compose (Recommended)
In the project root directory, run the following command to start the FastAPI app and Redis server simultaneously:

```bash
docker compose up --build
```

The application will be available at http://localhost:8000.

**Note: If Docker errors occur**

- Credential error (`docker-credential-desktop.exe` or similar): Run `docker logout` and retry.
- Buildx plugin error: Disable BuildKit using `DOCKER_BUILDKIT=0 docker compose up --build`

   
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

### Example CLI Commands
   ```bash
    curl "http://127.0.0.1:8000/rss/search?q=ai"
    curl "http://127.0.0.1:8000/rss/keys"
    curl -X DELETE "http://127.0.0.1:8000/rss/cache"
   ```

## 5. API Endpoints
- GET /rss/search?q={keyword}: Searches for news by keyword. Returns cached data if available, otherwise fetches new RSS data.
- GET /rss/metrics: Returns the number of cache hits and misses.
- GET /rss/keys: Returns a list of all rss:* keys stored in Redis.
- GET /rss/cache: Returns all cached rss:* data.
- DELETE /rss/cache: Deletes all cached data.
- DELETE /rss/cache/{keyword}: Deletes cached data for the given keyword.

## 6.Performance Testing

The `performance_test.py` script compares performance between fetching RSS feeds directly and using Redis cache.

**Command:**
```bash
python -m tests.performance_test [keyword]
```

- `[keyword]`: Optional keyword for the test (default is `fastapi` if omitted).

**Test steps:**
1. Clear all existing cached data.
2. Fetch RSS data directly and measure elapsed time.
3. Save the fetched data into Redis.
4. Fetch the cached data from Redis and compare the elapsed time to evaluate performance gain.

## 7. Future Plans
- Study Redis internals and implement a mini-Redis clone using C++.
- Replace Redis with the custom mini-Redis implementation in this project to compare real-world performance. [![GitHub](https://img.shields.io/badge/mini_redis-181717?style=flat&logo=github&logoColor=white)](https://github.com/DongInSong/mini-redis)
