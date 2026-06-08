from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)  # type: ignore

SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_session():
    async with SessionLocal() as session:
        yield session
