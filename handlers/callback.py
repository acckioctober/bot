from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram import types, Dispatcher


sync def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(MessageNotModified):
        await message.edit_text(f"Укажите число: {new_value}", reply_markup=get_keyboard_fab())


@dp.message_handler(commands="numbers_fab")
async def cmd_numbers(message: types.Message):
    data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())


async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
    user_value = data.get(call.from_user.id, 0)
    action = callback_data["action"]
    if action == "incr":
        data[call.from_user.id] = user_value + 1
        await update_num_text_fab(call.message, user_value + 1)
    elif action == "decr":
        data[call.from_user.id] = user_value - 1
        await update_num_text_fab(call.message, user_value - 1)
    await call.answer()


async def callbacks_num_finish_fab(call: types.CallbackQuery):
    user_value = data.get(call.from_user.id, 0)
    await call.message.edit_text(f"Итого: {user_value}")
    await call.answer()


def register_hanallback_query_handlers(dp: Dispatcher):
    '''Функция '''
    dp.register_callback_query_handler(callbacks_num_change_fab,
                                       callback=callback_numbers.filter(action=["incr", "decr"]))
    dp.register_callback_query_handler(callbacks_num_finish_fab,
                                       callback=callback_numbers.filter(action=["finish"]))