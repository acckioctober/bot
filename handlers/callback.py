from aiogram import types, Dispatcher
from keyboards.buttons import get_keyboard_for_gallery, \
    keyboard_for_start_construction_cake, keyboard_for_start_construction_cake_by_taste, \
    keyboard_for_start_construction_cake_by_type, \
    keyboard_for_handle_sort_callback
from config import bot
from database.bot_db import get_product_list, get_product_data, save_order_data, get_sorted_data_from_db, get_desrription
from keyboards.buttons import get_keyboard_for_start_order

async def callback_recent_gallery(call: types.CallbackQuery):
    product_list, cake_descriptions = get_product_list()
    for product, cake_description in zip(product_list, cake_descriptions):
        keyboard = types.InlineKeyboardMarkup()
        # Добавление кнопки "Хочу такой!" в InlineKeyboardMarkup
        keyboard.add(types.InlineKeyboardButton(text='Хочу такой!',
                                                callback_data=f'want_this_{product[0]}'))
        await bot.send_photo(call.from_user.id, product[7],
                             caption=f'{product[0]}.\n'
                                     f'Описание: {cake_description}\n'
                                     f'Вкус: {product[1]}.\n'
                                     f'Наполнитель: {product[2]}.\n'
                                     f'Топпинг: {product[3]}.\n'
                                     f'Вес: {product[4]} кг.\n'
                                     f'Цена: {product[5]} руб.\n',
                             reply_markup=keyboard)


async def callback_want_this(call: types.CallbackQuery):
        # Получение идентификатора товара из callback_data
        cake_type = call.data.split('_')[2]
        # Получение данных о товаре из базы данных
        product_data = get_product_data(cake_type)
        # Получение данных о пользователе
        user_id = call.from_user.id
        user_full_name = call.from_user.full_name
        # Получение других данных о пользователе, если необходимо
        # Сохранение данных в таблицу "Orders" в базе данных
        save_order_data(user_id, user_full_name, product_data)
        # Отправка сообщения "Спасибо" пользователю
        await bot.send_message(call.from_user.id,
                               f'Благодарим за Ваш заказ. {cake_type} это всегда отличный выбор! \n'
                               f'Мы с вами скоро свяжемся.',
                               reply_markup=get_keyboard_for_gallery())


async def callback_no_thanks(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Хорошего Вам настрояния!')


# async def start_construction_cake(call: types.CallbackQuery):
#     await bot.send_message(call.from_user.id, 'Начните с подбора по вкусу или по виду желаемого торта',
#                            reply_markup=keyboard_for_start_construction_cake())


async def start_construction_cake(call: types.CallbackQuery):
    # await bot.send_message(call.from_user.id, 'Начните свой выбор',
    #                        reply_markup=keyboard_for_start_construction_cake())
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=keyboard_for_start_construction_cake())

async def handle_sort_back_to_menu(query: types.CallbackQuery):
    keyboard = get_keyboard_for_start_order()
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        reply_markup=keyboard)

async def handle_sort_callback(query: types.CallbackQuery):
    global field
    field = query.data.split('_')[1]  # Извлекаем поле для сортировки
    keyboard = keyboard_for_handle_sort_callback(field)
    await bot.edit_message_reply_markup(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        reply_markup=keyboard)


async def handle_want_this_callback(query: types.CallbackQuery):
    data = query.data.split('_')[2]  # Извлекаем данные из callback_data
    if field == 'cake':
        key = f'{field}_type'
    else:
        key = field
    table_name = f'{field}s'
    descr = f'{field}_description'
    desrription = get_desrription(descr, table_name, key, data)
    await bot.send_message(query.from_user.id, f'{desrription[0]}')








# async def start_construction_cake_by_taste(call: types.CallbackQuery):
#     await bot.send_message(call.from_user.id, 'Выберите вкус',
#                            reply_markup=keyboard_for_start_construction_cake_by_taste(),
#                            disable_notification=True)
#
#     # await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=keyboard)
#
#
#     # await bot.send_message(call.from_user.id, 'q',
#     #                     reply_markup=keyboard_for_start_construction_cake_by_taste(),
#     #                     disable_notification=True)
#
#     # await bot.send_message(call.from_user.id, "Изначальная клавиатура",
#     #                        reply_markup=keyboard_for_start_construction_cake_by_taste())
#
#     # Некоторая логика, которая приводит к необходимости изменить клавиатуру
#
#     # await bot.edit_message_reply_markup(chat_id=call.from_user.id,
#     #                                     message_id=call.message.message_id,
#     #                                     reply_markup=keyboard_for_start_construction_cake_by_type())
#
#
#     # await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=message.message_id,
#     #                                     reply_markup=keyboard_for_start_construction_cake_by_type())
#
#
# # async def start_construction_cake_by_type(call: types.CallbackQuery):
# #     await bot.send_message(call.from_user.id, '\u200B',  # Пустая строка в качестве текста
# #                            reply_markup=keyboard_for_start_construction_cake_by_type(),
# #                            disable_notification=True)
#
# async def start_construction_cake_by_type(call: types.CallbackQuery):
#     await bot.send_message(call.from_user.id, 'Выберите тип торта',  # Неразрывный пробел в качестве текста
#                            reply_markup=keyboard_for_start_construction_cake_by_type(),
#                            disable_notification=True)



def register_callback_query_handlers(dp: Dispatcher):
    '''Функция регистрации обработчиков кнопок'''
    dp.register_callback_query_handler(callback_recent_gallery, text='recent_gallery')
    dp.register_callback_query_handler(callback_want_this, lambda c: c.data.startswith('want_this'))
    dp.register_callback_query_handler(callback_no_thanks, text='no_thanks')
    dp.register_callback_query_handler(start_construction_cake, text=['constructor',
                                                                      'вack_to_menu_start_construction_cake'])
    # dp.register_callback_query_handler(start_construction_cake_by_taste, text='choose_cake_by_taste')
    # dp.register_callback_query_handler(start_construction_cake_by_type, text='choose_cake_by_type')
    dp.register_callback_query_handler(handle_sort_callback,
                                       lambda query: query.data.startswith('sort_'))

    dp.register_callback_query_handler(handle_want_this_callback,
                                       lambda query: query.data.startswith('get_this_'))

    dp.register_callback_query_handler(handle_sort_back_to_menu,  text="back_to_menu")