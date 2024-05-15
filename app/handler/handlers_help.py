from aiogram import F,Router,Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import asyncio

from config import TOKEN, OWNER
from app.buttons.button import inline_keyboard_with_back_button

bot = Bot(token=TOKEN)


router_help = Router()

flag = False


 
@router_help.message(F.text == '/help')
async def help_command(message: Message):
    await message.answer("https://t.me/NNSSEEDD")





@router_help.callback_query(F.data == "techsupport")
async def techsupport(call: CallbackQuery):
     
    global flag
    await call.answer()
    await call.message.edit_text('Пожалуйста, введите ваш вопрос:', reply_markup=inline_keyboard_with_back_button)
    flag = True


@router_help.message(F.text)
async def process_techsupport_question(message: Message):
    global flag
    print(message.text)
    if flag:
        question = message.text
        user_id = message.from_user.id
        username = message.from_user.username

        recipient_id = OWNER
        user_link = f"Вопрос: {question}\nОтправлен от пользователя: https://t.me/{username}" if username else f"user_id: {user_id}"
        await bot.send_message(recipient_id, user_link)
        sent_message = await message.reply("Ваш вопрос был отправлен. В ближайшее время с вами свяжется наша техподдержка.")

        await asyncio.sleep(10)
        await sent_message.delete()

    else:
        await message.reply("Пожалуйста, сначала нажмите на кнопку 'Техподдержка' и введите ваш вопрос.")
