import time
from typing import Awaitable, Callable
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.context import correlation_id_context
from app.core.logging import Logger


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to generate and manage a unique `correlation` ID for each request.
    This correlation ID is stored in a context variable, allowing it to be accessed
    throughout the request lifecycle for logging purposes.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        correlation_id = request.headers.get("X-Correlation-Id", str(uuid.uuid4()))
        token = correlation_id_context.set(correlation_id)

        try:
            response = await call_next(request)
            response.headers["X-Correlation-Id"] = correlation_id
            return response
        finally:
            correlation_id_context.reset(token)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming HTTP requests and their corresponding responses.
    It captures the HTTP method, request path, response status code, and the duration of the request.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        Logger.log(
            "completed_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response
