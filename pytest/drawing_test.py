import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from raspberry_health.drawing import get_data, draw_plot
from datetime import datetime
from time import time
from fixtures import detached_engine, filled_sessionmaker, begining_time

@pytest.mark.asyncio
async def test_gathering(filled_sessionmaker: async_sessionmaker[AsyncSession], begining_time: float):
    date = datetime.fromtimestamp(begining_time - 3600)
    res = await get_data(filled_sessionmaker, date)
    assert len(res) > 1
    first = res[0]
    assert type(first[0]) is datetime and type(first[1]) is float
    print(res[0], res[-1])

@pytest.mark.asyncio
async def test_drawing(filled_sessionmaker: async_sessionmaker[AsyncSession], begining_time: float):
    date = datetime.fromtimestamp(begining_time - 3600)
    draw_plot(await get_data(filled_sessionmaker, date), "pic.png")
