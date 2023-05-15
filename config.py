from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os


load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
