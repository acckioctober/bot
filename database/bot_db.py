import sqlite3
from sqlite3 import Error
import random
from config import bot
from aiogram import types, Dispatcher
from keyboards.bottons import get_keyboard_for_gallery

def sql_create():
    global db, cursor
    db = sqlite3.connect('bot.db')
    cursor = db.cursor()
    if db:
        print('База подключена!')
    create = '''CREATE TABLE IF NOT EXISTS bot_tab
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                username VARCHAR (255),
                cake TEXT,
                weight FLOAT,
                name TEXT,
                address TEXT,
                apartment_floor TEXT,
                phone TEXT,
                add_information TEXT,
                delivery TEXT,
                payment_methods TEXT)'''
    db.execute(create)
    db.commit()

async def sql_command_insert(state):
    async with state.proxy() as data:
        sql = '''INSERT INTO bot_tab (tg_id, username, cake, weight, name, 
                address, apartment_floor, phone, add_information, 
                delivery, payment_methods) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
        cursor.execute(sql, tuple(data.values()))
        db.commit()

async def get_data(message: types.Message):
    results = cursor.execute('''SELECT * FROM bot_tab''').fetchall()
    random_data = random.choice(results)
    await bot.send_photo(message.from_user.id, random_data[-3])
    print('Запрос исполнен')


async def callback_recent_gallery(call: types.CallbackQuery):
    results = cursor.execute('''SELECT * FROM bot_tab''').fetchall()
    random_data = random.choice(results)
    await bot.send_photo(call.from_user.id, random_data[-3], reply_markup=get_keyboard_for_gallery())


def request_db(dp: Dispatcher):
    '''Функция регистрации обработчиков'''
    dp.register_message_handler(get_data, commands=['photo'])

def register_callback_query(dp: Dispatcher):
    dp.register_callback_query_handler(callback_recent_gallery, text='recent_gallery')