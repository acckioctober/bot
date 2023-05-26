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
from keyboards.buttons import get_keyboard_for_start_order

class FSMAdmin(StatesGroup):
    cake = State()
    weight = State()
    name = State()
    address = State()
    apartment_floor = State()
    phone = State()
    add_information = State()
    delivery = State()
    payment_methods = State()
    submit = State()


async def start(message: types.Message):
    if message.chat.type == 'private':
        await message.answer('Какой хотите заказать торт?',
                             reply_markup=get_keyboard_for_start_order())
    else:
        await message.answer('Пишите пожалуйста в личку!')

async def fsm_start(message: types.Message):
        await FSMAdmin.cake.set()
        await message.answer('Выберете тип торта', reply_markup=get_keyboard_for_cake())


async def load_cake(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tg_id'] = message.from_user.id
        data['username'] = f'@{message.from_user.username}'
        data['cake'] = message.text
    await FSMAdmin.next()
    await message.reply('Отличный выбор!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Укажите вес: 0", reply_markup=get_keyboard_fab())


async def load_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = message.text
    await FSMAdmin.next()
    await message.answer('Как Вас зовут?', reply_markup=types.ReplyKeyboardRemove())


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Введите адрес доставки')


async def load_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await FSMAdmin.next()
    await message.answer('Введите номер квартиры и этаж')


async def load_apartment_floor(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['apartment_floor'] = message.text
    await FSMAdmin.next()
    await message.answer('Введите номер телефона')


async def load_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await FSMAdmin.next()
    await message.answer('Введите доп. информацию или пришлите фото с изображением как образец для декорации на торте')


async def load_add_information(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.photo:
            data['add_information'] = message.photo[0].file_id
        else:
            data['add_information'] = message.text
    await FSMAdmin.next()
    await message.answer('Выберете способ доставки', reply_markup=get_keybord_for_cake_delivery())


async def load_delivery(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery'] = message.text
        await FSMAdmin.next()
        await message.answer('Выберете способ оплаты', reply_markup=get_keybord_for_payment_methods())


async def load_payment_methods(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['payment_methods'] = message.text
        await FSMAdmin.next()
        await message.answer('Подвердите правильность предоставленной информации',
                             reply_markup=get_keybord_for_submit())
        await message.answer_photo(data['add_information'])


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await sql_command_insert(state)
        #database
        await state.finish()
        await message.answer('Спасибо, Ваш заказ принят!', reply_markup=types.ReplyKeyboardRemove())
    elif message.text.lower() == 'нет':
        await state.finish()
        await message.answer('Вы можете пробовать заказать еще раз!', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_ordering(dp: Dispatcher):
    # dp.register_message_handler(fsm_start, commands='order')
    dp.register_message_handler(start, commands='order')
    dp.register_message_handler(load_cake, state=FSMAdmin.cake)
    dp.register_message_handler(load_weight, state=FSMAdmin.weight)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_address, state=FSMAdmin.address)
    dp.register_message_handler(load_apartment_floor, state=FSMAdmin.apartment_floor)
    dp.register_message_handler(load_phone, state=FSMAdmin.phone)
    dp.register_message_handler(load_add_information, state=FSMAdmin.add_information,
                                content_types=['photo', 'text'])
    dp.register_message_handler(load_delivery, state=FSMAdmin.delivery)
    dp.register_message_handler(load_payment_methods, state=FSMAdmin.payment_methods)
    dp.register_message_handler(load_submit, state=FSMAdmin.submit)
