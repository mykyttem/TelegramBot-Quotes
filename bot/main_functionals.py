from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import random
import asyncio
import os
import json

from config import dp, ref


# read file
folder_path = "results_scrapy"

# path file
file_path = os.path.join(folder_path, "quotes.json")

with open(file_path, 'r', encoding='utf-8') as file:
    quotes = json.load(file)



""" Main functionals """

# start buttons
start_btns = [
    [types.KeyboardButton(text='Запуск ✈')],
    [types.KeyboardButton(text='Налаштування ⚙')],
    [types.KeyboardButton(text='Мої улюблені цитати 📝💖')],
    [types.KeyboardButton(text="Зв'язок 💬")],
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
            {"id": id_user, "time-quotes": 1800, "favorite": [0], "category": "Всі"}
        )


@dp.message_handler(Text(equals=['Запуск ✈']))
async def launching(message: types.Message, state: FSMContext):
    """ Send quotes from file, and inline btn 'add favorite', save in DB num quote """
    
    # save value False, if launching start loop, else stop. Pass next handler
    async with state.proxy() as data:
        data['should_stop'] = False    

    # data user
    username = message.from_user.username
    user_data = ref.child(username).get()
    user_time_quotes = user_data.get("time-quotes")
    user_category = user_data.get("category")

    # send quote
    await message.answer('Запустилося✅\n По стандарту, буде відправляти кожні пів години одну цитату, можете змінити в налаштуваннях')

    while True:
        data = await state.get_data()
        should_stop = data.get('should_stop', False)

        if should_stop:
            break

        random_num = random.randint(0, 3000)
        
        try:
            btns_add_favorite = [
                [types.InlineKeyboardButton(text="Добавити в улюблені 📝", callback_data=f"add_favorite_{random_num}")]
            ]
            keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_add_favorite)

            quote = quotes[random_num]
            text = quote["text"]
            author = quote["author"]
            category = quote["category"]

            if user_category == "Всі":

                result = f"{text}\n Автор - {author}\n Категорія - {category}"

                await message.answer(result, reply_markup=keyboard_btns)
                await asyncio.sleep(user_time_quotes)

            elif user_category == category:

                result = f"{text}\n Автор - {author}\n Категорія - {category}"

                await message.answer(result, reply_markup=keyboard_btns)
                await asyncio.sleep(user_time_quotes)


        except IndexError:
            continue


@dp.message_handler(Text(equals=['Зупинити ❌']))
async def stop(message: types.Message, state: FSMContext):

    # save variable True, if user stopping loop 
    async with state.proxy() as data:
        data['should_stop'] = True

    await message.answer('Зупинено ⏱❌')
    

@dp.message_handler(Text(equals=['Назад ⏪']))
async def btn_back(message: types.Message):
    await message.answer('Головне меню', reply_markup=keyboard_start_btns)