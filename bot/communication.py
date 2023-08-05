from aiogram import types
from aiogram.dispatcher.filters import Text

from config import dp, bot


""" Сommunication """

@dp.message_handler(Text(equals=["Зв'язок 💬"]))
async def communication(message: types.Message):

    btns_communication = [
        [types.InlineKeyboardButton(text='Підтримка', callback_data='communication_support')],
        [types.InlineKeyboardButton(text='Пропозиція або Ідея', callback_data='communication_idea')],
    ]

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_communication)
    await message.answer('Оберіть вам потрібна підтримка, чи у вас є ідея?', reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('communication_'))
async def choice_communication(callback_query: types.CallbackQuery):
    """ We ask from the user write message, example: support or idea 
        after sending message, user who accept message users """

    # type message
    await callback_query.answer()
    choice_communication = callback_query.data.split('_')[1]

    # user write text
    username = callback_query.from_user.username
    await callback_query.message.answer("Введіть повідомлення")

    # sending message
    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    async def communcation_user_text(message: types.Message):
        user_text = message.text 

        # id who accept message from users
        await bot.send_message("id", f"""
            Повідомлення від користувача - @{username}
            Тип - {choice_communication}
            Текст:
            {user_text}
        """)