from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import redis.exceptions

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": "HTTP Exception",
            "message": exc.detail
        },
    )
    
async def redis_connection_error_handler(request: Request, exc: redis.exceptions.ConnectionError):
    return JSONResponse(
        status_code=503,
        content={
            "success": False,
            "error": "Redis connection error",
            "message": "Failed to connect to the Redis server. Please check your Redis configuration and ensure the server is running."
        },
    )


async def redis_response_error_handler(request: Request, exc: redis.exceptions.ResponseError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": "Redis response error",
            "message": f"An error occurred while processing the request to Redis. This may be due to an invalid command or data format.: {str(exc)}"
        },
    )

async def redis_timeout_error_handler(request: Request, exc: redis.exceptions.TimeoutError):
    return JSONResponse(
        status_code=504,
        content={
            "success": False,
            "error": "Redis timeout error",
            "message": "Redis server did not respond in time. Please try again later or check the server status."
        },
    )
    
async def redis_generic_error_handler(request: Request, exc: redis.exceptions.RedisError):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Redis generic error",
            "message": str(exc)
        },
    )
    
def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(redis.exceptions.ConnectionError, redis_connection_error_handler)
    app.add_exception_handler(redis.exceptions.ResponseError, redis_response_error_handler)
    app.add_exception_handler(redis.exceptions.TimeoutError, redis_timeout_error_handler)
    app.add_exception_handler(redis.exceptions.RedisError, redis_generic_error_handler)