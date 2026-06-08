from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.core.logging import logging_config
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.middleware import RequestLoggingMiddleware, CorrelationIDMiddleware
from app.core.tracing import tracing_config

logging_config()
tracing_config()

app = FastAPI(
    title="Mars Probe Simulator",
    description=(
        "A production-style backend API for simulating Mars probes, built with FastAPI. "
        "It demonstrates a clean layered architecture, async-first design, PostgreSQL-ready "
        "persistence, and endpoints for probe setup, movement, and status checks."
    ),
)

Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app, excluded_urls="^/metrics$")

app.include_router(api_router, prefix="/api/v1")
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(CorrelationIDMiddleware)
