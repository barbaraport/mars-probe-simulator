from alembic import command
from alembic.config import Config
import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from app.core.config import settings

TEST_DB_URL = str(settings.DATABASE_URL)


@pytest.fixture(scope="session", autouse=True)
def migrate_database():
    alembig_config = Config("alembic.ini")
    alembig_config.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembig_config, "head")
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
