from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import bot, ADMINS
from keyboards.buttons import get_keyboard_for_add_photo, get_keybord_for_submit
from database.bot_db import sql_commands_apdate


class FSMAdmin(StatesGroup):
    get_photo  = State()
    get_cake_type = State()
    submit = State()


async def fsm_start(message: types.Message):
    await FSMAdmin.get_photo.set()
    await message.answer('Пришлите фото')

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer('Выберети тип торта', reply_markup=get_keyboard_for_add_photo())


async def load_cake_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['cake_type'] = message.text
    await FSMAdmin.next()
    await message.answer('Подтвердите правильность', reply_markup=get_keybord_for_submit())
    await message.answer_photo(data['photo'], caption=data['cake_type'])


async def load_submit(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        await sql_commands_apdate(state)
        await state.finish()
        await message.answer('Спасибо, изменения внесены!', reply_markup=types.ReplyKeyboardRemove())
    elif message.text.lower() == 'нет':
        await state.finish()
        await message.answer('Вы можете пробовать еще раз!', reply_markup=types.ReplyKeyboardRemove())


def register_handlers_crud(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands='admin')
    dp.register_message_handler(load_photo, state=FSMAdmin.get_photo, content_types=['photo'])
    dp.register_message_handler(load_cake_type, state=FSMAdmin.get_cake_type)
    dp.register_message_handler(load_submit, state=FSMAdmin.submit)
