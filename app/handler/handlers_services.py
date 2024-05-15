
from aiogram import F,Router,Bot
from aiogram.types import Message, CallbackQuery,InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command 
from app.DB.request import get_groups, get_services_by_group, get_service_by_id, save_appeal_to_database
from aiogram.fsm.context import FSMContext
import re
from config import TOKEN,OWNER
router_services = Router()

from app.buttons.button  import inline_keyboard, inline_keyboard_with_back_button,inline_keyboard_back_to_services
from app.buttons.state import ServicesState

bot = Bot(TOKEN)


@router_services.callback_query(F.data == "Services")
async def show_groups(call: CallbackQuery):
    groups = await get_groups()
    buttons = []
    
    for group in groups:
        buttons.append([InlineKeyboardButton(text=group.name, callback_data=f"show_services_{group.id}")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]) 
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.edit_text("Выберите группу товаров:", reply_markup=keyboard)
    await call.answer()


@router_services.callback_query(F.data.startswith("show_services_"))
async def show_services(call: CallbackQuery):
    group_id = int(call.data.split("_")[-1])
    print(group_id)
    services = await get_services_by_group(group_id)
    if services:
        buttons = []
        for service in services:
            buttons.append([InlineKeyboardButton(text=service.name, callback_data=f"service_{service.id}_{group_id}")])
        
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="Services")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons, max_button_width=200)  # Устанавливаем ширину кнопок в пикселях
        await call.message.edit_text("Выберите услугу:", reply_markup=keyboard)
    else:
        await call.message.edit_text("В этой группе нет доступных товаров.", reply_markup=inline_keyboard_with_back_button)
    await call.answer()


@router_services.callback_query(F.data.startswith("service_"))
async def service(call: CallbackQuery, state: FSMContext):
    # Извлекаем service_id и group_id из данных обратного вызова
    service_id = int(call.data.split("_")[1])
    group_id = int(call.data.split("_")[2])
    
    # Получаем выбранную услугу по ее ID и ID группы
    service = await get_service_by_id(service_id, group_id)
    
    if service:
        await state.set_state(ServicesState.sevrice_id)
        await state.update_data(service_id=service.name)
        await state.set_state(ServicesState.name)
        message_text = f"{service.name}\n"
        
        if service.description:
            message_text += f"Описание: {service.description}\n"
        
        if service.price:
            message_text += f"Цена: {service.price}\n"
 
        # Редактируем сообщение с информацией об услуге
        await call.message.edit_text(message_text, reply_markup=inline_keyboard_back_to_services)
    else:
        await call.message.edit_text("Не удалось получить информацию о выбранной услуге.", reply_markup=inline_keyboard_back_to_services)
    
    await call.answer()


@router_services.callback_query(F.data == "Send_data")
async def send_data(call: CallbackQuery,state:FSMContext):
    await state.set_state(ServicesState.name)
    await call.message.edit_text('Введите ФИО')

@router_services.message(ServicesState.name)
async def get_name(call: CallbackQuery,state:FSMContext):
    await state.update_data(name=call.text)
    await state.set_state(ServicesState.phone)
    await call.answer('Введите номер телефона')


@router_services.message(ServicesState.phone)
async def get_phone(call: CallbackQuery,state:FSMContext):
    if not call.text.isdigit():
        await call.answer('Номер телефона должен состоять только из цифр')
        return
    await state.update_data(phone=call.text)
    await state.set_state(ServicesState.message)
    await call.answer('Введите сообщение')


@router_services.message(ServicesState.message)
async def get_message(call: CallbackQuery, state: FSMContext):
    await state.update_data(message=call.text)
    data = await state.get_data()
    await state.clear()
    data['tg_id'] = call.from_user.id
    data['service_id'] = data.get('service_id')
    # Сохраняем данные обращения в базу данных
    print(data)

    text = f"Услуга: {data.get('service_id')}\nФИО: {data.get('name')}\nТелефон: {data.get('phone')}\nСообщение: {data.get('message')}"
    await save_appeal_to_database(data)
    await bot.send_message(OWNER, f"Новое обращение: {text}\n https://t.me/{call.from_user.username}")
    await call.answer('Спасибо за обращение', reply_markup=inline_keyboard_with_back_button)