from aiogram import executor
from aiogram import types
from aiogram.dispatcher.filters import Text

from config import dp
from firebase_config import ref
from vsviti_motivation import quotes

import time


# beginning meny
@dp.message_handler(commands=['start'])
async def start_btns(message: types.Message):

    # start buttons
    start_btns = [
        [types.KeyboardButton(text='Запуск ✈')],
        [types.KeyboardButton(text='Налаштування ⚙')],
        [types.KeyboardButton(text='Зупинити ❌')],
    ]

    keyboard_btns = types.ReplyKeyboardMarkup(keyboard=start_btns, resize_keyboard=True)

    await message.answer(f'Привіт {message.from_user.first_name}, це бот, якого задача мотивувати тебе\n В налаштуваннях можеш налаштувати систему сповіщень або інше', 
                        reply_markup=keyboard_btns
    )


    # Getting data for user
    id_user = str(message.from_id)
    username = message.from_user.username

    # push data
    if not ref.child(username).get():
        ref.child(username).set({"id": id_user, "time-quotes": "30 minutes"})


@dp.message_handler(Text(equals=['Запуск ✈']))
async def launching(message: types.Message):

    await message.answer('Запустилося✅\n По стандарту, від буде відправляти кожні пів години, одну цитату, можете змінити в налаштуваннях')

    for i in range(100):

        # 30 minutes
        time.sleep(1800)
        await message.answer(quotes[i])



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)