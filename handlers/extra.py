from aiogram import types
from config import bot, Dispatcher


async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)

def register_handlers_extra(dp: Dispatcher):
    '''Функция регистрации обработчиков сообщений в модуле extra'''
    dp.register_message_handler(echo)