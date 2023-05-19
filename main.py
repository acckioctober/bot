from aiogram import executor
from config import dp
from handlers import client
from handlers import extra
from handlers import fsm_bot_ordering


fsm_bot_ordering.register_handlers_ordering(dp)
client.register_handlers_client(dp)
extra.register_handlers_extra(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
