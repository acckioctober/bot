from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.button import (get_keyboard_for_cake,
                            get_keyboard_fab,
                            get_keybord_for_cake_delivery,
                            get_keybord_for_payment_methods,
                            get_keybord_for_submit)
from database.bot_db import sql_command_insert
from keyboards.bottons import get_keyboard_for_start_order
from aiogram.utils.callback_data import CallbackData
from config import bot

class FSMAdmin(StatesGroup):
    start_order = State()
    choose_flavor  = State()
    choose_toppings  = State()
    enter_details  = State()
    confirm_order  = State()
    save_order  = State()
    view_orders  = State()
    track_order  = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        # await FSMAdmin.start_order.set()
        await message.answer('Какой хотите заказать торт?',
                             reply_markup=get_keyboard_for_start_order())
    else:
        await message.answer('Пишите пожалуйста в личку!')


# async def callback_recent_gallery(call: types.CallbackQuery):
#     # print(call)
#     # await bot.send_message(call.from_user.id, "Hy")
#     results = cursor.execute('''SELECT * FROM bot_tab''').fetchall()
#     random_data = random.choice(results)
#     await bot.send_photo(call.from_user.id, random_data[-3])



def register_handlers_ordering(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands='order')

# def register_callback_query(dp: Dispatcher):
#     dp.register_callback_query_handler(callback_recent_gallery, text='recent_gallery')
