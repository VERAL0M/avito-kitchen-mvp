import os
from collections.abc import AsyncIterator

import pytest
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from auth.infrastructure.persistence_sqla.mappings.map import map_tables
from auth.infrastructure.persistence_sqla.orm_registry import mapping_registry


# SQLAlchemy maps these domain classes once per Python process.
if not mapping_registry.mappers:
    map_tables()


@pytest.fixture
async def db_session_factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    database_url = os.getenv("TEST_DATABASE_URL")
    if not database_url:
        pytest.fail("Set TEST_DATABASE_URL to the dedicated order_test database")

    database_name = make_url(database_url).database
    if database_name != "order_test":
        pytest.fail(
            "Integration tests may only create/drop tables in the order_test database"
        )

    engine = create_async_engine(database_url)
    metadata = mapping_registry.metadata

    try:
        async with engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)

        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        async with engine.begin() as connection:
            await connection.run_sync(metadata.drop_all)
        await engine.dispose()


@pytest.fixture
async def db_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with db_session_factory() as session:
        yield session
