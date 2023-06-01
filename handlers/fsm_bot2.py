from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.bot_db import sql_command_insert
from keyboards.buttons import get_keyboard_for_start_order
from aiogram.utils.callback_data import CallbackData
from config import bot
from keyboards.buttons import get_keyboard, keyboard_for_handle_sort_callback

class FSMAdmin(StatesGroup):
    # start_order = State()
    choose_cake_type = State()
    choose_taste = State()
    choose_filling = State()
    choose_topping = State()
    choose_weight_kg = State()
    # choose_date = State()
    submit = State()

    # enter_details  = State()
    # confirm_order  = State()
    # save_order  = State()
    # view_orders  = State()
    # track_order  = State()


# Обработчик команды /start для начала заказа
async def start_order(message: types.Message):
    await FSMAdmin.choose_cake_type.set()
    await message.reply("Добро пожаловать в процесс заказа!")
    await message.answer("Выберите тип торта:",
                        reply_markup=keyboard_for_handle_sort_callback('cake'))

async def update_start_order_text(message: types.Message, new_value: str):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"Выберите тип торта: {new_value}",
                        reply_markup=keyboard_for_handle_sort_callback('cake'))

async def load_cake_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        action = call.data
        if action.startswith('get_'):
            cake_type = action.split("_")[2]
            data['cake_type'] = cake_type
            await update_start_order_text(call.message, cake_type)
        elif action.startswith('вack_') and 'cake_type' in data:
            await call.message.edit_text(f"Тип торта: {data['cake_type']}")
            await FSMAdmin.next()
            await call.message.reply("Выберите вкус торта:")
        await call.answer()


# async def load_cake_type(message: types.Message, state: FSMContext):
#     # cake_type = message.text
#     # await state.update_data(cake_type=cake_type)
#     async with state.proxy() as data:
#         data['cake_type'] = message.text
#     await FSMAdmin.next()
#     await message.reply("Выберите вкус торта:")


async def load_taste(message: types.Message, state: FSMContext):
    # taste = message.text
    # await state.update_data(taste=taste)
    async with state.proxy() as data:
        data['taste'] = message.text
    await FSMAdmin.next()
    await message.reply("Выберите начинку для торта:")


async def load_filling(message: types.Message, state: FSMContext):
    # filling = message.text
    # await state.update_data(filling=filling)
    async with state.proxy() as data:
        data['filling'] = message.text
    await FSMAdmin.next()
    await message.reply("Выберите topping для торта:")


async def load_topping(message: types.Message, state: FSMContext):
    selected_toppings = message.text.split(",") # Разделение выбранных topping по запятой
    toppings_dict = {topping: True for topping in selected_toppings} # Формирование словаря с использованием генератора словаря
    async with state.proxy() as data:
        data['topping'] = toppings_dict
        data['user_data'] = {message.from_user.id: 0}  # Сохранение данных о значениях кнопок в контексте состояния
    await FSMAdmin.next()
    await message.reply("Укажите число: 0", reply_markup=get_keyboard())


async def update_num_text(message: types.Message, new_value: int):
    # Общая функция для обновления текста с отправкой той же клавиатуры
    await message.edit_text(f"Укажите число: {new_value}", reply_markup=get_keyboard())


async def load_weight_kg(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        user_data = data['user_data']  # Получение данных о значениях кнопок из контекста состояния
        user_value = user_data.get(call.from_user.id, 0) # Получаем текущее значение для пользователя, либо считаем его равным 0?
        action = call.data.split("_")[1]
        if action == "incr":
            user_data[call.from_user.id] = user_value + 1
            await update_num_text(call.message, user_value + 1)
            print(user_data)
        elif action == "decr":
            user_data[call.from_user.id] = user_value - 1
            await update_num_text(call.message, user_value - 1)
            print(user_data)
        elif action == "finish":
            await call.message.edit_text(f"Итого: {user_value}")
            await FSMAdmin.next()
            # await call.message.reply("Пожалуйста, выберите дату:", reply_markup=handle_date_command())
            # await call.message.answer('Подвердите правильность предоставленной информации')
            # Не забываем отчитаться о получении колбэка
        await call.answer()










async def load_submit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    await state.finish()
    await message.answer('Спасибо, Ваш заказ принят!')



# И так далее, обработчики для остальных состояний

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     dp.middleware.setup(FSMContextMiddleware())
#     executor.start_polling(dp, skip_updates=True)


def register_handlers_ordering(dp: Dispatcher):
    dp.register_message_handler(start_order, commands='starts')
    # dp.register_message_handler(load_cake_type, state=FSMAdmin.choose_cake_type)

    dp.register_callback_query_handler(load_cake_type, lambda call: call.data.startswith('get_this_'),
                                        state=FSMAdmin.choose_cake_type)
    dp.register_callback_query_handler(load_cake_type,
                                       lambda call: call.data.startswith('вack_to_'), state=FSMAdmin.choose_cake_type)


    dp.register_message_handler(load_taste, state=FSMAdmin.choose_taste)
    dp.register_message_handler(load_filling, state=FSMAdmin.choose_filling)
    dp.register_message_handler(load_topping, state=FSMAdmin.choose_topping)
    # dp.register_message_handler(load_weight_kg, state=FSMAdmin.choose_weight_kg)

    # dp.register_callback_query_handler(callbacks_num_change_fab,
    #                                    callback_numbers.filter(action=["incr", "decr"]),
    #                                    state=FSMAdmin.choose_topping)
    # dp.register_callback_query_handler(callbacks_num_finish_fab,
    #                                    callback_numbers.filter(action=["finish"]),
    #                                    state=FSMAdmin.choose_topping)

    # dp.register_callback_query_handler(load_weight_kg, lambda call: call.data.startswith('num_'),
    #                                     state=FSMAdmin.choose_weight_kg)

    # dp.callback_query_handler(callbacks_num, lambda call: call.data.startswith('num_'),
    #                                     state=FSMAdmin.choose_weight_kg)




    # dp.register_callback_query_handler(get_order, lambda query: query.data == "get_order", state="*")
    # dp.register_callback_query_handler(handle_date_picker, lambda query: query.data == "date_picker"
    #                                    , state=FSMAdmin.choose_date)

    dp.register_message_handler(load_submit, state=FSMAdmin.submit)







