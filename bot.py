
import logging
from config import Config as c

from tortoise import Tortoise, run_async
from models import User

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keyboards import *


logging.basicConfig(level=c.LOG_LEVEL)

bot = Bot(token=c.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user = await User.filter(tg_id=message.from_user.id).first()
    if not user:
        user = User(tg_id=message.from_user.id, username=message.from_user.username)
        await user.save()

    await message.answer(f"Hi, {user.username}", reply_markup=main_menu())


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


async def init_db():
    await Tortoise.init(
        db_url=f'postgres://{c.DB_USER}:{c.DB_PASS}@{c.DB_HOST}:{c.DB_PORT}/{c.DB_NAME}',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    run_async(init_db())
    executor.start_polling(dp)
