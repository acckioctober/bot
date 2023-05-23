from aiogram import types
from aiogram.utils.callback_data import CallbackData


def get_keyboard_for_start_order():
    ''''''
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
                types.InlineKeyboardButton(text="Недавно люди выбирали", callback_data='recent_gallery'),
                types.InlineKeyboardButton(text="Попробовать конструктор", callback_data='constructor')
    ]
    keyboard.add(*buttons)
    return keyboard

def get_keyboard_for_gallery():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text="хочу такой!", callback_data='want_this'),
        types.InlineKeyboardButton(text="выйти", callback_data='quit'),
        types.InlineKeyboardButton(text="посмотреть еще", callback_data='recent_gallery')
    ]
    keyboard.add(*buttons)
    return keyboard