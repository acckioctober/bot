from aiogram import executor
from config import dp
from handlers import client
from handlers import extra
from handlers import fsm_bot_ordering
from database.bot_db import sql_create, register_callback_query

# from handlers import fsm_bot2

async def on_startup(_):
    sql_create()

# fsm_bot2.register_handlers_ordering(dp)
register_callback_query(dp)
fsm_bot_ordering.register_handlers_ordering(dp)
client.register_handlers_client(dp)
# bot_db.request_db(dp)
# extra.register_handlers_extra(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup = on_startup)

