import aiogram
import asyncio
 
from aiogram import F,Bot, Dispatcher 
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart
 
 
from config import TOKEN
from app.handler.handlers_help import router_help
from app.handler.handlers_main import router_main
from app.handler.handlers_services import router_services
from app.DB.models import create_db


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    await create_db()
    print('Бот запущен')
    dp.include_routers(router_main,router_services,router_help)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
