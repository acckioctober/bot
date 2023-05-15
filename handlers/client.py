from aiogram import types, Dispatcher
from random import choice
import os
from handlers.button import get_keyboard_for_start


async def start_method(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}!', reply_markup=get_keyboard_for_start())


async def help_method(message: types.Message):
    await message.answer(f'/start - приветствие по имени\n'
                         f'/myinfo - посмотреть свои данные (id, first_name, username)\n'
                         f'/picture - посмотреть картинку отобранную случайным образом\n'
                         f'/help - список команд')


async def my_info_method(message: types.Message):
    await message.answer(f'Ваш id: {message.from_user.id}\n'
                         f'Ваше имя: {message.from_user.first_name}\n'
                         f'Ваш username: @{message.from_user.username}')


async def random_picture_method(message: types.Message):
    with open(os.path.join('images', choice(os.listdir('images'))), 'rb') as photo:
        await message.answer_photo(photo)


def register_handlers_client(dp: Dispatcher):
    '''Функция регистрации обработчиков сообщений в модуле client'''
    dp.register_message_handler(start_method, commands=['start'])
    dp.register_message_handler(help_method, commands=['help'])
    dp.register_message_handler(my_info_method, commands=['myinfo'])
    dp.register_message_handler(random_picture_method, commands=['picture'])


