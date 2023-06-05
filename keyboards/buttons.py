from aiogram import types, Dispatcher
from database.bot_db import get_button_names_from_product_table, \
    get_button_names_from_relation_table_by_cake_taste, \
    get_button_names_from_relation_table_by_cake_type, \
    get_sorted_data_from_db
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData
from contextlib import suppress
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



def keyboard_for_start_construction_cake():
    # keyboard = types.InlineKeyboardMarkup(row_width=1)
    # buttons = [
    #     types.InlineKeyboardButton(text="Выбрать по вкусу торта", callback_data='choose_cake_by_taste'),
    #     types.InlineKeyboardButton(text="Выбрать по виду торта", callback_data='choose_cake_by_type')
    # ]
    # keyboard.add(*buttons)
    # return keyboard

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_cake = types.InlineKeyboardButton("По cake", callback_data="sort_cake")
    button_taste = types.InlineKeyboardButton("По taste", callback_data="sort_taste")
    button_filling = types.InlineKeyboardButton("По filling", callback_data="sort_filling")
    button_topping = types.InlineKeyboardButton("По topping", callback_data="sort_topping")
    button_back_to_menu = types.InlineKeyboardButton("Назад к меню", callback_data="back_to_menu")
    keyboard.add(button_cake, button_taste, button_filling, button_topping, button_back_to_menu)
    return keyboard

# def keyboard_for_handle_sort_callback(field):
#     sorted_data = get_sorted_data_from_db(field)  # Получаем отсортированные данные из базы данных
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     buttons = []
#     for data in sorted_data:
#         buttons.append(types.InlineKeyboardButton(text=f'{data[0]}', callback_data=f'want_this_{data[0]}'))
#     keyboard.add(*buttons)
#     return keyboard


def keyboard_for_handle_sort_callback(field):
    sorted_data = get_sorted_data_from_db(field) # Получаем отсортированные данные из базы данных
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for data in sorted_data:
        callback_data = f'get_this_{data[0]}'  # Формируем значение callback_data
        button = types.InlineKeyboardButton(text=f'{data[0]}', callback_data=callback_data)
        keyboard.add(button)
    keyboard.add(types.InlineKeyboardButton(text='Назад к меню',
                                            callback_data='вack_to_menu_start_construction_cake'))
    return keyboard









def keyboard_for_start_construction_cake_by_taste():
    # button_names = get_button_names_from_relation_table_by_cake_taste()
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # for button_name in button_names:
    #     button = types.KeyboardButton(text=button_name[0])
    #     keyboard.add(button)

    button_names = get_button_names_from_relation_table_by_cake_taste()
    keyboard = types.InlineKeyboardMarkup()
    # Добавление кнопки "Хочу такой!" в InlineKeyboardMarkup
    for button_name in button_names:
        keyboard.add(types.InlineKeyboardButton(text=f'{button_name[0]}',
                                            callback_data=f'want_this_{button_name[0]}'))
    return keyboard














# def keyboard_for_start_construction_cake_by_taste():
#     # button_names = get_button_names_from_relation_table_by_cake_taste()
#     # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     # for button_name in button_names:
#     #     button = types.KeyboardButton(text=button_name[0])
#     #     keyboard.add(button)
#     button_names = get_button_names_from_relation_table_by_cake_taste()
#     keyboard = types.InlineKeyboardMarkup()
#     # Добавление кнопки "Хочу такой!" в InlineKeyboardMarkup
#     for button_name in button_names:
#         keyboard.add(types.InlineKeyboardButton(text=f'{button_name[0]}',
#                                             callback_data=f'want_this_{button_name[0]}'))
#     return keyboard


def keyboard_for_start_construction_cake_by_type():
    # button_names = get_button_names_from_relation_table_by_cake_type()
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # for button_name in button_names:
    #     button = types.KeyboardButton(text=button_name[0])
    #     keyboard.add(button)
    button_names = get_button_names_from_relation_table_by_cake_type()
    keyboard = types.InlineKeyboardMarkup()
    # Добавление кнопки "Хочу такой!" в InlineKeyboardMarkup
    for button_name in button_names:
        keyboard.add(types.InlineKeyboardButton(text=f'{button_name[0]}',
                                            callback_data=f'want_this_{button_name[0]}'))
    return keyboard







#
# callback_numbers = CallbackData("fabnum", "action")
# def get_keyboard_fab():
#     buttons = [
#     types.InlineKeyboardButton(text="-1", callback_data=callback_numbers.new(action="decr")),
#     types.InlineKeyboardButton(text="+1", callback_data=callback_numbers.new(action="incr")),
#     types.InlineKeyboardButton(text="Подтвердить", callback_data=callback_numbers.new(action="finish"))
#     ]
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard
# #
#
def get_keyboard():
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
        types.InlineKeyboardButton(text="+1", callback_data="num_incr"),
        types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_ban_button():
    # Генерация клавиатуры для администратора.
    buttons = [
        types.InlineKeyboardButton(text="Забанить", callback_data="ban"),
        types.InlineKeyboardButton(text="Разбанить", callback_data="unban"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

