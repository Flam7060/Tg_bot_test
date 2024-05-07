from aiogram import F,Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

router_main = Router()

from app.buttons.button  import inline_keyboard, inline_keyboard_with_back_button
from app.templates.tempate import start_message, abaout_us
from app.templates.tempate import contactss
 

@router_main.message(CommandStart())
async def start(message: Message) -> None:
    global flag
    # Отправка приветственного сообщения
    await message.answer(start_message, reply_markup=inline_keyboard)
    flag = False

@router_main.callback_query(F.data == "Contacts")
async def contacts(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(contactss, reply_markup=inline_keyboard_with_back_button)


@router_main.callback_query(F.data == "about_us")
async def about_us(call: CallbackQuery):
    await call.answer('')
    await call.message.edit_text(
        abaout_us, reply_markup=inline_keyboard_with_back_button
    )


@router_main.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(call: CallbackQuery):
    await call.answer('')
    await call.message.edit_text(start_message, reply_markup=inline_keyboard)

