from aiogram import types
from config import bot, Dispatcher


async def echo(message: types.Message):
    if message.chat.type == 'private': # Если это личный чат с ботом, просто выйти из функции
        return
    bad_words = ['плохо', 'ужасно', 'отвратительно']
    name = f"@{message.from_user.username}" if message.from_user.username is not None else message.from_user.first_name
    # Получаем список администраторов чата
    administrators = await bot.get_chat_administrators(message.chat.id)
    # Проверяем является ли нарушитель администратором
    is_admin = any(admin.user.id == message.from_user.id for admin in administrators)
    if message.text.lower() in bad_words:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=f"Забанить {name}",
                                                callback_data=f"ban_{message.from_user.id}"))
        if is_admin:
            await message.reply('Пожалуйста, уважайте правила группы даже если вы администратор!')
        else:
            await message.reply(f'{name} нарушает правила группы употребляя плохие слова!',
                                reply_markup=keyboard)


async def ban_user(call: types.CallbackQuery):
    user_id = call.data.split('_')[1]
    name = f"@{call.message.reply_to_message.from_user.username}" if call.message.reply_to_message.from_user.username \
                                                    is not None else call.message.reply_to_message.from_user.first_name
    await bot.kick_chat_member(call.message.chat.id, user_id)
    await bot.delete_message(call.message.reply_to_message.chat.id, call.message.reply_to_message.message_id)
    await call.message.delete()
    await bot.send_message(call.message.chat.id, f'{name} был удален из чата администратором!')
    await bot.send_message(user_id, f'Вы были удалены из чата {call.message.chat.title} администратором!')


def register_handlers_extra(dp: Dispatcher):
    '''Функция регистрации обработчиков сообщений в модуле extra'''
    dp.register_message_handler(echo)
    dp.register_callback_query_handler(ban_user, lambda call: call.data.startswith("ban_"))