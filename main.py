from aiogram import executor
from config import dp
from handlers import client
from handlers import extra
from handlers import fsm_bot_ordering
from database.bot_db import sql_create, insert_data, request_db
from handlers import callback
from handlers import fsm_bot2
from handlers import add_photo_fsm
from handlers import apscheduler

async def on_startup(_):
    sql_create()
    # insert_data()


fsm_bot2.register_handlers_ordering(dp)
# callback.register_callback_query_handlers(dp)
add_photo_fsm.register_handlers_crud(dp)
fsm_bot_ordering.register_handlers_ordering(dp)
client.register_handlers_client(dp)
request_db(dp)
extra.register_handlers_extra(dp)

apscheduler.register_handlers_apscheduler(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup = on_startup)

