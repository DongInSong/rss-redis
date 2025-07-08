import sys
import time
from app.rss_reader import fetch_rss
from app.redis_client import get_cached_news, set_cached_news, delete_all_cache, get_all_keys

class PerformanceTester:
    def __init__(self, query):
        if not query:
            raise ValueError("Query parameter cannot be empty.")
        self.query = query

    def run_test(self):
        # 기존 캐시 삭제
        delete_all_cache()
        
        print("--- 캐시 성능 테스트 시작 ---")

        # RSS fetch 시간 측정
        print(f"\n1. RSS 피드 fetch. value: {self.query}")
        start_time = time.time()
        news_data = fetch_rss(self.query)
        end_time = time.time()
        fetch_duration_ms = (end_time - start_time) * 1000
        print(f"경과 시간: {fetch_duration_ms:.2f} ms")

        # 캐시 저장
        set_cached_news(self.query, news_data)
        print(f"\n2. 캐시 저장 완료. {get_all_keys()}")

        # Redis 캐시 데이터 호출 시간 측정
        print("\n3. Redis 캐시 데이터 호출")
        start_time = time.time()
        get_cached_news(self.query)
        end_time = time.time()
        cache_duration_ms = (end_time - start_time) * 1000
        print(f"경과 시간: {cache_duration_ms:.2f} ms")

        # 결과
        print("\n--- 테스트 결과 ---")
        print(f"RSS Fetch: {fetch_duration_ms:.2f} ms")
        print(f"Redis 캐시 호출: {cache_duration_ms:.2f} ms")
        
        if fetch_duration_ms > cache_duration_ms:
            performance_improvement = fetch_duration_ms / cache_duration_ms
            print(f"\n캐시 사용 시 약 {performance_improvement:.2f}배 성능 향상!")
        else:
            print("\n캐시 사용이 fetch보다 느리거나 동일합니다.")
        
        delete_all_cache()
        print("\n--- 테스트 완료. 모든 캐시를 삭제했습니다. ---")
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = "fastapi"  # 기본 키워드
    
    print(f"선택된 테스트 키워드: '{keyword}'")
    tester = PerformanceTester(query=keyword)
    tester.run_test()

