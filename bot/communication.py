from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import dp, bot
from .main_functionals import l_trans

""" Сommunication """

@dp.message_handler(Text(equals=["Зв'язок 💬", "Communication 💬"]))
async def communication(message: types.Message, state: FSMContext):

    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')


    btns_communication = [
        [types.InlineKeyboardButton(text=l_trans('Підтримка', user_language), callback_data='communication_support')],
        [types.InlineKeyboardButton(text=l_trans('Пропозиція або Ідея', user_language), callback_data='communication_idea')],
    ]

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_communication)
    await message.answer(l_trans('Оберіть вам потрібна підтримка, чи у вас є ідея?', user_language), reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('communication_'))
async def choice_communication(callback_query: types.CallbackQuery, state: FSMContext):
    """ We ask from the user write message, example: support or idea 
        after sending message, user who accept message users """


    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')


    # type message
    await callback_query.answer()
    choice_communication = callback_query.data.split('_')[1]

    # user write text
    username = callback_query.from_user.username
    await callback_query.message.answer(l_trans("Введіть повідомлення", user_language))

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