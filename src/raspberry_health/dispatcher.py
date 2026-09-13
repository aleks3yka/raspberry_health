from aiogram import Dispatcher, F
from aiogram.types import Message, FSInputFile
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from raspberry_health.drawing import get_data, draw_plot
from datetime import datetime
from time import time
from re import Match

root = Dispatcher()

@root.message(F.text.regexp("^(\\d+)$").as_("hours"))
async def send_plot(message: Message, hours: Match[str], session_maker: async_sessionmaker[AsyncSession]):
    print("here")
    timeDelta = int(hours.group(1)) * 3600

    data = await get_data(session_maker, datetime.fromtimestamp(time() - timeDelta))
    if len(data) == 0:
        message.answer("No data")
        return
    pic_name = str(message.chat.id) + "pic.png"
    draw_plot(data, pic_name)

    await message.reply_photo(FSInputFile(pic_name))

@root.message()
async def echo(message: Message):
    # print("echoing")
    await message.answer("HI!")
