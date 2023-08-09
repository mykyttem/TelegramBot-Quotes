from aiogram import types
from aiogram.dispatcher.filters import Text

from config import dp, ref
from .main_functionals import trans


""" Settings """

@dp.message_handler(Text(equals=['Налаштування ⚙', 'Settings ⚙']))
async def settings(message: types.Message):

    # Getting user data
    username = message.from_user.username
    user_data = ref.child(username).get()
    user_language = user_data.get("language")

    btns_settings = [
        [types.KeyboardButton(text=trans('Час відправки цитати ⏱', dest=user_language).text)],
        [types.KeyboardButton(text=trans('Категорія 🧾', dest=user_language).text)],
        [types.KeyboardButton(text=trans('Назад ⏪', dest=user_language).text)]
    ]

    keyboard_btns = types.ReplyKeyboardMarkup(keyboard=btns_settings, resize_keyboard=True)
    await message.answer(trans('Налаштування', dest=user_language).text, reply_markup=keyboard_btns)


@dp.message_handler(Text(equals=['Час відправки цитати ⏱', 'Quote sending time ⏱']))
async def time_send_quote(message: types.Message):
    # Getting user data
    username = message.from_user.username
    user_data = ref.child(username).get()
    user_language = user_data.get("language")

    btns_time = []

    # Add buttons for 30 minutes and hours 1 to 24 in separate rows
    btns_time.append([types.InlineKeyboardButton(text='0.5', callback_data='time_0.5')])
    for i in range(1, 25):
        btns_time.append([types.InlineKeyboardButton(text=trans(f'{i} години', dest=user_language).text, callback_data=f'time_{i}')])

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_time)

    await message.answer(trans('Оберіть через скільки часу вам відправляти', dest=user_language), reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('time_'))
async def choice_time(callback_query: types.CallbackQuery):
    # Getting user data
    username = callback_query.from_user.username
    user_data = ref.child(username).get()
    user_language = user_data.get("language")

    await callback_query.answer()

    time_value = float(callback_query.data.split('_')[1])
    await callback_query.message.answer(f'Ви обрали {time_value} години/hours')

    # change data user
    username = callback_query.from_user.username
    user_data = ref.child(username).get()

    # convert hours in seconds
    seconds = int(time_value * 3600)

    # update
    user_data["time-quotes"] = int(seconds)
    ref.child(username).update(user_data)

    await callback_query.message.answer(trans('Налаштування оновлені ✅', dest=user_language).text) 


@dp.message_handler(Text(equals=['Категорія 🧾', 'Category 🧾']))
async def settings_category(message: types.Message):

    # Getting user data
    username = message.from_user.username
    user_data = ref.child(username).get()
    user_language = user_data.get("language")


    btns_category = [
        [types.InlineKeyboardButton(text=trans('з Книг 📚', dest=user_language).text, callback_data='category_з Книг')],
        [types.InlineKeyboardButton(text=trans('з Фільмів 🎬', dest=user_language).text, callback_data='category_з Фільмів')],
        [types.InlineKeyboardButton(text=trans('Відомих людей', dest=user_language).text, callback_data='category_Відомих людей')],
        [types.InlineKeyboardButton(text=trans('Всі', dest=user_language).text, callback_data='category_Всі')],
    ]

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_category)
    await message.answer(trans('Оберіть категорію цитат', dest=user_language).text, reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('category_'))
async def choice_category_settings(callback_query: types.CallbackQuery):
    # Getting user data
    username = callback_query.from_user.username
    user_data = ref.child(username).get()
    user_language = user_data.get("language")

    await callback_query.answer()

    select_category = callback_query.data.split('_')[1]

    # change data user
    username = callback_query.from_user.username
    user_data = ref.child(username).get()

    # update
    user_data["category"] = select_category
    ref.child(username).update(user_data)

    
    await callback_query.message.answer(trans('Налаштування оновлені ✅', dest=user_language).text) 
    await callback_query.message.answer(trans(select_category, dest=user_language).text ) 