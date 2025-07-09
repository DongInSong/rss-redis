from fastapi import Request
from fastapi.responses import JSONResponse
import redis.exceptions

async def redis_connection_error_handler(request: Request, exc: redis.exceptions.ConnectionError):
    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error": "Redis 연결 오류",
            "message": "Redis 서버 연결에 실패했습니다."
        },
    )

async def redis_response_error_handler(request: Request, exc: redis.exceptions.ResponseError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": "Redis 명령어 오류",
            "message": f"Redis에서 지원하지 않거나 잘못된 명령어입니다: {exc}"
        },
    )
