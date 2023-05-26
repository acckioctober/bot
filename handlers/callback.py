from aiogram import types, Dispatcher
from keyboards.buttons import get_keyboard_for_gallery
from config import bot
from database.bot_db import get_product_list, get_product_data, save_order_data


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


def register_callback_query_handlers(dp: Dispatcher):
    '''Функция регистрации обработчиков кнопок'''
    dp.register_callback_query_handler(callback_recent_gallery, text='recent_gallery')
    dp.register_callback_query_handler(callback_want_this, lambda c: c.data.startswith('want_this'))
    dp.register_callback_query_handler(callback_no_thanks, text='no_thanks')