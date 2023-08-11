from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from config import dp, ref
from .main_functionals import l_trans


""" Settings """

@dp.message_handler(Text(equals=['Налаштування ⚙', 'Settings ⚙']))
async def settings(message: types.Message, state: FSMContext):

    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')


    btns_settings = [
        [types.KeyboardButton(text=l_trans('Час відправки цитати ⏱', user_language))],
        [types.KeyboardButton(text=l_trans('Категорія 🧾', user_language))],
        [types.KeyboardButton(text=l_trans('Назад ⏪', user_language))]
    ]

    keyboard_btns = types.ReplyKeyboardMarkup(keyboard=btns_settings, resize_keyboard=True)
    await message.answer(l_trans('Налаштування', user_language), reply_markup=keyboard_btns)


@dp.message_handler(Text(equals=['Час відправки цитати ⏱', 'Quote sending time ⏱']))
async def time_send_quote(message: types.Message, state: FSMContext):
    # Getting user data

    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')

    btns_time = []

    # Add buttons for 30 minutes and hours 1 to 24 in separate rows
    btns_time.append([types.InlineKeyboardButton(text='0.5', callback_data='time_0.5')])
    for i in range(1, 25):
        btns_time.append([types.InlineKeyboardButton(text=f'{i} години / hours', callback_data=f'time_{i}')])

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_time)

    await message.answer(l_trans('Оберіть через скільки часу вам відправляти', user_language), reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('time_'))
async def choice_time(callback_query: types.CallbackQuery, state: FSMContext):

    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')


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

    await callback_query.message.answer(l_trans('Налаштування оновлені ✅', user_language)) 


@dp.message_handler(Text(equals=['Категорія 🧾', 'Category 🧾']))
async def settings_category(message: types.Message, state: FSMContext):

    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')


    btns_category = [
        [types.InlineKeyboardButton(text=l_trans('з Книг 📚', user_language), callback_data='category_з Книг')],
        [types.InlineKeyboardButton(text=l_trans('з Фільмів 🎬', user_language), callback_data='category_з Фільмів')],
        [types.InlineKeyboardButton(text=l_trans('Відомих людей', user_language), callback_data='category_Відомих людей')],
        [types.InlineKeyboardButton(text=l_trans('Всі', user_language), callback_data='category_Всі')],
    ]

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_category)
    await message.answer(l_trans('Оберіть категорію цитат', user_language), reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('category_'))
async def choice_category_settings(callback_query: types.CallbackQuery, state: FSMContext):
  
    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')

    await callback_query.answer()

    select_category = callback_query.data.split('_')[1]

    # change data user
    username = callback_query.from_user.username
    user_data = ref.child(username).get()

    # update
    user_data["category"] = select_category
    ref.child(username).update(user_data)

    
    await callback_query.message.answer(l_trans('Налаштування оновлені ✅', user_language)) 
    await callback_query.message.answer(l_trans(select_category, user_language)) 