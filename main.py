from aiogram import executor
from config import dp
from handlers import client
from handlers import extra


client.register_handlers_client(dp)
extra.register_handlers_extra(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
