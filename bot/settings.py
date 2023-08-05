from aiogram import types
from aiogram.dispatcher.filters import Text

from config import dp, ref


""" Settings """

@dp.message_handler(Text(equals=['Налаштування ⚙']))
async def settings(message: types.Message):
    btns_settings = [
        [types.KeyboardButton(text='Час відправки цитати ⏱')],
        [types.KeyboardButton(text='Категорія 🧾')],
        [types.KeyboardButton(text='Назад ⏪')]
    ]

    keyboard_btns = types.ReplyKeyboardMarkup(keyboard=btns_settings, resize_keyboard=True)
    await message.answer('Налаштування', reply_markup=keyboard_btns)


@dp.message_handler(Text(equals=['Час відправки цитати ⏱']))
async def time_send_quote(message: types.Message):
    btns_time = []

    # Add buttons for 30 minutes and hours 1 to 24 in separate rows
    btns_time.append([types.InlineKeyboardButton(text='0.5', callback_data='time_0.5')])
    for i in range(1, 25):
        btns_time.append([types.InlineKeyboardButton(text=f'{i} години', callback_data=f'time_{i}')])

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_time)

    await message.answer('Оберіть через скільки часу вам відправляти', reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('time_'))
async def choice_time(callback_query: types.CallbackQuery):
    await callback_query.answer()

    time_value = float(callback_query.data.split('_')[1])
    await callback_query.message.answer(f'Ви обрали {time_value} години')

    # change data user
    username = callback_query.from_user.username
    user_data = ref.child(username).get()

    # convert hours in seconds
    seconds = int(time_value * 3600)

    # update
    user_data["time-quotes"] = int(seconds)
    ref.child(username).update(user_data)

    await callback_query.message.answer('Налаштування оновлені ✅') 


@dp.message_handler(Text(equals=['Категорія 🧾']))
async def settings_category(message: types.Message):

    btns_category = [
        [types.InlineKeyboardButton(text='з Книг 📚', callback_data='category_з Книг')],
        [types.InlineKeyboardButton(text='з Фільмів 🎬', callback_data='category_з Фільмів')],
        [types.InlineKeyboardButton(text='Відомих людей', callback_data='category_Відомих людей')],
        [types.InlineKeyboardButton(text='Всі', callback_data='category_Всі')],
    ]

    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_category)
    await message.answer('Оберіть категорію цитат', reply_markup=keyboard_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('category_'))
async def choice_category_settings(callback_query: types.CallbackQuery):
    await callback_query.answer()

    select_category = callback_query.data.split('_')[1]

    # change data user
    username = callback_query.from_user.username
    user_data = ref.child(username).get()

    # update
    user_data["category"] = select_category
    ref.child(username).update(user_data)

    
    await callback_query.message.answer('Налаштування оновлені ✅') 
    await callback_query.message.answer(select_category) 