from matplotlib import pyplot
from typing import Sequence, Tuple
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from datetime import datetime
from raspberry_health.database import Measurement
from sqlalchemy import select
# from raspberry_health.database import Measurement

def draw_plot(dots: Sequence[Tuple[datetime, float]], filename: str):
    x, y = zip(*dots)

    fig, ax = pyplot.subplots()

    ax.plot(x, y)

    ax.set_xlabel("time")
    ax.set_ylabel("temp, C")

    fig.savefig(filename)
    pyplot.close(fig)

async def get_data(session_maker: async_sessionmaker[AsyncSession], date_from: datetime)\
      -> Sequence[Tuple[datetime, float]]:
    async with session_maker() as session:
        res = await session.execute(select(Measurement.date, Measurement.temperature))
    return res.all()
    