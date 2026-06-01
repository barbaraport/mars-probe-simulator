from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="Mars Probe Simulator",
    description=(
        "A production-style backend API for simulating Mars probes, built with FastAPI. "
        "It demonstrates a clean layered architecture, async-first design, PostgreSQL-ready "
        "persistence, and endpoints for probe setup, movement, and status checks."
    ),
)

app.include_router(api_router, prefix="/api/v1")
