from aiogram import types
from database.bot_db import get_button_names_from_product_table


def get_keyboard_for_start_order():
    ''''''
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
                types.InlineKeyboardButton(text="Недавно люди выбирали", callback_data='recent_gallery'),
                types.InlineKeyboardButton(text="Попробовать конструктор", callback_data='constructor')
    ]
    keyboard.add(*buttons)
    return keyboard

# def get_keyboard_for_gallery():
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     buttons = [
#         types.InlineKeyboardButton(text="хочу такой!", callback_data='want_this'),
#         types.InlineKeyboardButton(text="выйти", callback_data='quit'),
#         types.InlineKeyboardButton(text="посмотреть еще", callback_data='recent_gallery')
#     ]
#     keyboard.add(*buttons)
#     return keyboard


def get_keyboard_for_gallery():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="посмотреть еще!", callback_data='recent_gallery'),
        types.InlineKeyboardButton(text="нет спасибо!", callback_data='no_thanks')
    ]
    keyboard.add(*buttons)
    return keyboard



def get_keyboard_for_add_photo():
    button_names = get_button_names_from_product_table()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button_name in button_names:
        button = types.KeyboardButton(text=button_name[0])
        keyboard.add(button)
    return keyboard



def get_keybord_for_submit():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
            types.KeyboardButton(text="да"),
            types.KeyboardButton(text="нет")
    ]
    keyboard.add(*buttons)
    return keyboard