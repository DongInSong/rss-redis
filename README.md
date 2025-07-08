# Redis를 사용한 RSS 뉴스 피드 캐싱

## 1. 개요

FastAPI를 사용하여 특정 키워드에 대한 RSS 뉴스 피드를 파싱하고, Redis를 통해 검색 결과를 캐싱하여 응답 속도를 향상시키는 웹 서비스 기반 테스트 프로젝트입니다. API를 통해 실시간으로 뉴스를 검색하거나 캐시된 데이터를 빠르게 조회할 수 있습니다.

## 2. 주요 기능

- **키워드 기반 뉴스 검색**: 사용자가 원하는 키워드로 RSS 피드 검색
- **Redis 캐싱**: 한 번 검색된 결과는 Redis에 지정된 시간(TTL) 동안 캐시되어, 동일한 요청에 대해 더 빠른 응답 제공 'config,py'
- **캐시 통계**: 캐시 히트(hit) 및 미스(miss) 횟수 집계
- **데이터 조회**: Redis에 저장된 캐시 키 또는 전체 캐시 데이터 조회
- **성능 테스트**: 캐시 사용 유무에 따른 성능 차이를 비교하는 테스트 스크립트

## 3. 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)  ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)  ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)  

## 4. 설치 및 실행 방법

- ### Docker Compose를 사용한 실행 (권장)
>
> 프로젝트 루트 디렉토리에서 다음 명령어를 실행하면 FastAPI 애플리케이션과 Redis 데이터베이스를 한 번에 실행할 수 있습니다.
> 
> ```bash
> docker compose up --build
> ```
> 
> - 애플리케이션은 `http://localhost:8000`에서 실행됩니다.
> 
> **참고: Docker 실행 오류 시**
> 
> - **인증 오류 (`docker-credential-desktop.exe` or similar):** `docker logout` 실행 후 다시 시도
> - **`buildx` 플러그인 오류:** `DOCKER_BUILDKIT=0 docker compose up --build` 명령어로 실행하여 BuildKit을 비활성화


- ### 직접 실행
> 
> - Python 3.8 이상
> - Redis 서버
> 
> 1.  **프로젝트 클론**
>     ```bash
>     git clone https://github.com/DongInSong/rss-redis.git
>     cd rss-redis
>     ```
> 
> 2.  **의존성 설치**
>     ```bash
>     pip install -r requirements.txt
>     ```
> 
> 3.  **Redis 서버 실행 (docker)**   
>     ```bash
>     docker run --name redis -p 6379:6379 -d redis
>     ```
> 
> 4.  **서버 실행**
>     ```bash
>     uvicorn app.main:app --reload
>     ```

- ### CLI 테스트 예시
    ```bash
    curl "http://127.0.0.1:8000/rss/search?q=ai"
    curl "http://127.0.0.1:8000/rss/keys"
    curl -X DELETE "http://127.0.0.1:8000/rss/cache"
    ```

## 5. API 엔드포인트

- `GET /rss/search?q={keyword}`: 특정 키워드로 뉴스를 검색합니다. 캐시가 있으면 캐시된 데이터를, 없으면 RSS 피드를 직접 가져옵니다.
- `GET /rss/metrics`: 캐시 히트/미스 횟수를 조회합니다.
- `GET /rss/keys`: Redis에 저장된 모든 `rss:*` 키 목록을 반환합니다.
- `GET /rss/cache`: Redis에 저장된 모든 `rss:*` 키와 해당 데이터를 반환합니다.
- `DELETE /rss/cache`: Redis에 저장된 모든 `cache`를 제거합니다.
- `DELETE /rss/cache/{keyword}`: Redis에 저장된 keyword(value)에 해당되는 `cache`를 제거합니다.

## 6. 성능 테스트 방법

`performance_test.py` 는 RSS 피드를 직접 가져오는 것과 Redis 캐시를 사용하는 것 사이의 성능 차이를 측정합니다.

**실행 명령어:**

```bash
python -m tests.performance_test [keyword]
```

- `[keyword]`: 테스트할 검색어입니다. 이 인수를 생략하면 기본값인 "fastapi"로 테스트가 진행됩니다.

**테스트 순서:**
1.  기존의 모든 캐시 데이터를 삭제합니다.
2.  RSS 피드를 직접 fetch하여 경과 시간을 측정합니다.
3.  가져온 데이터를 Redis에 저장합니다.
4.  Redis에서 캐시된 데이터를 조회하여 경과 시간을 측정하고 성능 향상률을 출력합니다.

## 7. 차후 계획
- Redis 내부 구조에 대한 이해 및 C++로 mini-redis 직접 구현
- 현재 프로젝트에서 사용 중인 Redis를 mini-redis로 교체하여 실제 성능 비교 및 검증 진행
