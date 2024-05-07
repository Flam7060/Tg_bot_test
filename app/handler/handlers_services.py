
from aiogram import F,Router
from aiogram.types import Message, CallbackQuery,InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command 
from app.DB.request import get_groups, get_services_by_group

router_services = Router()

from app.buttons.button  import inline_keyboard, inline_keyboard_with_back_button,inline_keyboard_back_to_services 



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
    services = await get_services_by_group(group_id)
    if services:
        services_text = ""
        for index, service in enumerate(services, start=1):
            services_text += f"{index}. {service.name}\n"   
        
        # Создаем кнопки с номерами услуг
        buttons = []
        num_services = len(services)
        row_length = 3 if num_services % 2 != 0 else 4
        
        for index, _ in enumerate(services, start=1):
            if index % row_length == 1:
                buttons.append([])
            buttons[-1].append(InlineKeyboardButton(text=str(index), callback_data=f"service_{index}_{group_id}"))
        
        buttons.append([InlineKeyboardButton(text="Назад", callback_data="Services")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.edit_text(services_text, reply_markup=keyboard)
    else:
        await call.message.edit_text("В этой группе нет доступных товаров.", reply_markup=inline_keyboard_with_back_button)
    await call.answer()


@router_services.callback_query(F.data.startswith("service_"))
async def service(call: CallbackQuery):
    service_id = int(call.data.split("_")[-2])
    group_id = int(call.data.split("_")[-1])
    service = await get_services_by_group(group_id)
    
    if service:
        service = service[service_id - 1]
        message_text = f"{service.name}\n"
        
        if service.description:
            message_text += f"Описание: {service.description}\n"
        if service.price:
            message_text += f"Цена: {service.price}\n"
 

        await call.message.edit_text(message_text, reply_markup=inline_keyboard_back_to_services)
    else:
        await call.message.edit_text("Не удалось получить информацию о выбранной услуге.", reply_markup=inline_keyboard_back_to_services)
    
    await call.answer()


 