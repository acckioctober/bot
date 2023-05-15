from aiogram import types


def get_keyboard_for_start():
    '''Фукция для создания инлайн-кнопок для сообщения-ответа на команду start в модуле client'''
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
                types.InlineKeyboardButton(text="Geeks", url="https://geeks.edu.kg/"),
                types.InlineKeyboardButton(text="Оф. канал GeekNews", url="https://t.me/c/1212966386/640"),
                types.InlineKeyboardButton(text="Kурсы Geeks", url="https://geeks.edu.kg/#kurs")
    ]
    keyboard.add(*buttons)
    return keyboard
