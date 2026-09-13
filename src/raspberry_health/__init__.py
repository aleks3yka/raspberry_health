from raspberry_health.dispatcher import root
from raspberry_health.measuring import add_measurement, Temp_reader
from raspberry_health.database import Base
import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

async def async_main() -> None:
    token = getenv("BOT_TOKEN")
    if token is None:
        raise ValueError("no token in BOT_TOKEN env")
    tg_bot = Bot(token)

    engine = create_async_engine("sqlite+aiosqlite:///my.db")
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine)

    scheduler = AsyncIOScheduler()

    scheduler.add_job(add_measurement, "interval", [session_maker, Temp_reader()], minutes=1, id="temp reading")
    scheduler.start()

    await root.start_polling(tg_bot, session_maker=session_maker)

def main() -> None:
    asyncio.run(async_main())
