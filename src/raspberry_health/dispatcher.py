from aiogram import Dispatcher, F
from aiogram.types import Message, FSInputFile
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from raspberry_health.drawing import get_data, draw_plot
from datetime import datetime
from time import time

root = Dispatcher()

@root.message(F.regexp("^(\d+)$").as_("hours"))
async def send_plot(message: Message, hours: str, session_maker: async_sessionmaker[AsyncSession]):
    timeDelta = int(hours) * 3600

    data = await get_data(session_maker, datetime.fromtimestamp(time() - timeDelta))
    if len(data) == 0:
        message.answer("No data")
        return
    pic_name = message.chat.id + "pic.png"
    await draw_plot(data, pic_name)

    message.reply_photo(FSInputFile(pic_name))
