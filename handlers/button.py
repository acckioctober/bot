from aiogram import types
from aiogram.utils.callback_data import CallbackData


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

def get_keyboard_for_cake():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [
                types.KeyboardButton(text='Торты Гранд'),
                types.KeyboardButton(text='Торты бисквитные'),
                types.KeyboardButton(text='Торты муссовые'),
                types.KeyboardButton(text='Торты и чизкейки'),
                types.KeyboardButton(text='Торты слоеные и коржевые')
    ]
    keyboard.add(*buttons)
    return keyboard

def get_keybord_for_cake_delivery():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton(text='Доставьте заказ как можно скорее'),
        types.KeyboardButton(text='Выбрать дату и время доставки'),
    ]
    keyboard.add(*buttons)
    return keyboard

def get_keybord_for_payment_methods():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
            types.KeyboardButton(text="Оплата наличными курьеру"),
            types.KeyboardButton(text="оплата картой")
    ]
    keyboard.add(*buttons)
    return keyboard

def get_keybord_for_submit():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
            types.KeyboardButton(text="да"),
            types.KeyboardButton(text="нет")
    ]
    keyboard.add(*buttons)
    return keyboard


callback_numbers = CallbackData("fabnum", "action")
def get_keyboard_fab():
    buttons = [
        types.InlineKeyboardButton(text="-1", callback_data=callback_numbers.new(action="decr")),
        types.InlineKeyboardButton(text="+1", callback_data=callback_numbers.new(action="incr")),
        types.InlineKeyboardButton(text="Подтвердить", callback_data=callback_numbers.new(action="finish"))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard