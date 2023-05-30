from config import bot, scheduler
from aiogram import Dispatcher
import asyncio
from datetime import datetime, timedelta
from aiogram import types
from config import dp


async def start_scheduler():
    scheduler.start()


async def send_reminder(chat_id: int, reminder_text: str):
    await bot.send_message(chat_id=chat_id, text=reminder_text)


async def handle_reminder(message):
    reminder_text = message.text
    chat_id = message.chat.id
    # Установка напоминания через 5 секунд
    # reminder_time = datetime.now() + timedelta(seconds=5)
    # scheduler.add_job(send_reminder, 'date', run_date=reminder_time, args=(chat_id, reminder_text))
    scheduler.add_job(send_reminder, 'interval', seconds = 5, args=(chat_id, reminder_text))
    await message.reply("Напоминание установлено!")



async def start_handler(message: types.Message):
    'Oбработчик для команды /sched, который запускает планировщик'
    await message.answer("Привет! Я готов установить напоминания. Используйте команду /setreminder для этого.")
    # Запуск планировщика в асинхронном режиме
    asyncio.create_task(start_scheduler())


async def set_reminder_handler(message: types.Message):
    'Oбработчик для команды /setreminder, который вызывает функцию handle_reminder'
    await message.answer("Введите текст напоминания:")
    # Регистрируем следующий обработчик для получения текста напоминания
    dp.register_message_handler(handle_reminder, content_types=types.ContentTypes.TEXT)


def register_handlers_apscheduler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["sched"])
    dp.register_message_handler(set_reminder_handler, commands=["setreminder"])

