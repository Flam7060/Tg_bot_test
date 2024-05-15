from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



inline_buttons = [
    [InlineKeyboardButton(text="Услуги", callback_data="Services")],
    [InlineKeyboardButton(text="О нас", callback_data="about_us")],
    [InlineKeyboardButton(text="Контакты", callback_data="Contacts")],
    [InlineKeyboardButton(text="Техподдержка", callback_data="techsupport")]
]
inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_buttons)


inline_buttons_with_back = [
    [InlineKeyboardButton(text="В меню", callback_data="back_to_main_menu")]
]
inline_keyboard_with_back_button = InlineKeyboardMarkup(inline_keyboard=inline_buttons_with_back)


inline_buttons_back_to_services = [
    [InlineKeyboardButton(text="Отправить данные для связи", callback_data="Send_data")], # я хотел подключить покупку но не получилось 
    [InlineKeyboardButton(text="Назад", callback_data="Services")]
]
inline_keyboard_back_to_services = InlineKeyboardMarkup(inline_keyboard=inline_buttons_back_to_services)

 