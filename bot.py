from aiogram import executor
from aiogram import types
from aiogram.dispatcher.filters import Text

from config import dp
from firebase_config import ref
from vsviti_motivation import quotes

import time


""" Main functionals """

# start buttons
start_btns = [
    [types.KeyboardButton(text='Запуск ✈')],
    [types.KeyboardButton(text='Налаштування ⚙')],
    [types.KeyboardButton(text='Зупинити ❌')],
]
keyboard_start_btns = types.ReplyKeyboardMarkup(keyboard=start_btns, resize_keyboard=True)

# beginning menu
@dp.message_handler(commands=['start'])
async def start_btns(message: types.Message):

    await message.answer(f'Привіт {message.from_user.first_name}, це бот, якого задача мотивувати тебе\n В налаштуваннях можеш налаштувати систему сповіщень або інше', 
                        reply_markup=keyboard_start_btns
    )

    # Getting data for user
    id_user = str(message.from_id)
    username = message.from_user.username

    # push data
    if not ref.child(username).get():
        ref.child(username).set(
            {"id": id_user, "time-quotes": 1800}
        )


@dp.message_handler(Text(equals=['Запуск ✈']))
async def launching(message: types.Message):

    # data user
    username = message.from_user.username
    user_data = ref.child(username).get()
    user_time_quotes = user_data.get("time-quotes")

    # send quote
    await message.answer('Запустилося✅\n По стандарту, від буде відправляти кожні пів години, одну цитату, можете змінити в налаштуваннях')

    for i in range(100):

        time.sleep(user_time_quotes)
        await message.answer(quotes[i])


@dp.message_handler(Text(equals=['Назад ⏪']))
async def btn_back(message: types.Message):
    await message.answer('Головне меню', reply_markup=keyboard_start_btns)



""" Settings """

@dp.message_handler(Text(equals=['Налаштування ⚙']))
async def settings(message: types.Message):
    btns_settings = [
        [types.KeyboardButton(text='Час відправки цитати ⏱')],
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)