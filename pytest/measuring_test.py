import raspberry_health.measuring as measuring
import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from raspberry_health.database import Base, Measurement

def test_get_temp_zone():
    res = measuring.detect_thermalzone()
    print("device detected ", res)

def test_get_temp():
    path = measuring.detect_thermalzone()
    res = measuring.read_temp(path)
    assert 0 <= res <= 100
    print("temperature read ", res)

def test_class():
    reader = measuring.Temp_reader()
    assert 0 <= reader.get_temp() <= 100

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

@pytest.fixture
def temp_reader() -> measuring.Temp_reader:
    return measuring.Temp_reader()

@pytest.mark.asyncio
async def test_add_measurement(session_maker: async_sessionmaker[AsyncSession], temp_reader: measuring.Temp_reader):
    await measuring.add_measurement(session_maker, temp_reader)
    async with session_maker() as session:
        res = await session.execute(select(Measurement))
        count = len(res.all())
    assert count == 1
