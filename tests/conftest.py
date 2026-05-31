from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from app.core.config import settings
from app.core.database import get_session
from app.main import app

TEST_DB_URL = str(settings.DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def migrate_database():
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_config, "head")
    yield


@pytest_asyncio.fixture
async def test_session():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    test_session = async_sessionmaker(engine, expire_on_commit=False)

    async with test_session() as session:
        yield session
        await session.execute(
            text("""TRUNCATE TABLE grid, probe RESTART IDENTITY CASCADE""")
        )
        await session.commit()


@pytest_asyncio.fixture
async def client(test_session: AsyncSession):
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost/"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
