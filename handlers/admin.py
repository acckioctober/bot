from config import bot, ADMINS
from aiogram import types, Dispatcher


async def add_photo_to_db(message: types.Message):
    if message.from_user.id in ADMINS:
        photo = message.photo
        print(photo)



