from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from random import choice
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
DIR = 'images'


@dp.message_handler(commands=['start'])
async def start_method(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}!')


@dp.message_handler(commands=['help'])
async def help_method(message: types.Message):
    await message.answer(f'/start - приветствие по имени\n'
                         f'/myinfo - посмотреть свои данные (id, first_name, username)\n'
                         f'/picture - посмотреть картинку отобранную случайным образом\n'
                         f'/help - список команд')


@dp.message_handler(commands=['myinfo'])
async def myinfo_method(message: types.Message):
    await message.answer(f'Ваш id: {message.from_user.id}\n'
                         f'Ваше имя: {message.from_user.first_name}\n'
                         f'Ваш username: @{message.from_user.username}')


@dp.message_handler(commands=['picture'])
async def random_picture_method(message: types.Message):
    photo = open(os.path.join(DIR, choice(os.listdir(DIR))), 'rb')
    await message.answer_photo(photo)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
