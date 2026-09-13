import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from raspberry_health.database import Base, Measurement
from datetime import datetime
from math import sin

@pytest_asyncio.fixture
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///test.db")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest_asyncio.fixture
async def session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncEngine]:
    return async_sessionmaker(engine)

@pytest_asyncio.fixture
async def detached_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()

@pytest.fixture
def begining_time() -> float:
    return 3600.0

@pytest_asyncio.fixture
async def filled_sessionmaker(detached_engine: AsyncEngine, begining_time) -> async_sessionmaker[AsyncEngine]:
    session_maker = async_sessionmaker(detached_engine)

    measurements = [Measurement(source="cpu", date=datetime.fromtimestamp(begining_time - t), temperature=sin(t * 0.1 / 30))\
                    for t in range(0, 3600, 30)]

    async with session_maker() as session:
        session.add_all(measurements)
        await session.commit()

    return session_maker
