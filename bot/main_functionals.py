from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from googletrans import Translator

import random
import asyncio
import os
import json

from config import dp, ref

#TODO: added hand regimen

# read file
folder_path = "results_scrapy"

# path file
file_path = os.path.join(folder_path, "quotes.json")

with open(file_path, 'r', encoding='utf-8') as file:
    quotes = json.load(file)

# translate
trans = Translator().translate

""" Main functionals """
""" Using "state: FSMContext" for pass variables between functions """

# beginning menu
@dp.message_handler(commands=['start'])
async def choose_languages(message: types.Message):

    btns_language = [
        [types.KeyboardButton(text='Українська 🇺🇦')],
        [types.KeyboardButton(text='English 🇺🇸')]
    ]

    keyboard_start_languages = types.ReplyKeyboardMarkup(keyboard=btns_language, resize_keyboard=True)

    await message.answer(f'Оберіть мову\n choose a language', reply_markup=keyboard_start_languages)


@dp.message_handler(Text(equals=['Українська 🇺🇦', 'English 🇺🇸']))
async def beginning_btns(message: types.Message, state: FSMContext):

    if message.text == "Українська 🇺🇦":
        language = "uk"
    elif message.text == "English 🇺🇸":
        language = "en"


    # start buttons
    start_btns = [
        [types.KeyboardButton(text=trans('Запуск ✈', dest=language).text)],
        [types.KeyboardButton(text=trans('Ручний режим', dest=language).text)],
        [types.KeyboardButton(text=trans('Налаштування ⚙', dest=language).text)],
        [types.KeyboardButton(text=trans('Мої улюблені цитати 📝💖', dest=language).text)],
        [types.KeyboardButton(text=trans("Зв'язок 💬", dest=language).text)],
        [types.KeyboardButton(text=trans('Зупинити ❌', dest=language).text)],
    ]
    keyboard_start_btns = types.ReplyKeyboardMarkup(keyboard=start_btns, resize_keyboard=True)


    txt = trans("Привіт, це бот, якого задача мотивувати тебе В налаштуваннях можеш налаштувати систему сповіщень або інше", dest=language).text
    await message.answer(txt, reply_markup=keyboard_start_btns)


    # Getting data for user
    id_user = str(message.from_id)
    username = message.from_user.username

    # push data
    if not ref.child(username).get():
        ref.child(username).set(
            {"id": id_user, "time-quotes": 1800, "favorite": [0], "category": "Всі", "language": language} 
        )


    user_data = ref.child(username).get()
    user_time_quotes = user_data.get("time-quotes")
    user_category = user_data.get("category")
    user_language = user_data.get("language")
    user_favorite = user_data.get("favorite")

    # Save variables for other functions - data user
    async with state.proxy() as data:
        data['should_stop'] = False    
        data['user_time_quotes'] = user_time_quotes
        data['user_category'] = user_category
        data['user_favorite'] = user_favorite
        data['user_language'] = user_language


@dp.message_handler(Text(equals=['Запуск ✈', 'Launch ✈']))
async def launching(message: types.Message, state: FSMContext):
    """ Send quotes from file, and inline btn 'add favorite', save in DB num quote """


    # save value False, if launching start loop, else stop. Pass next handler. 
    # Save variables for other functions - data user
    async with state.proxy() as data:
        data['should_stop'] = False   
        user_time_quotes = data.get('user_time_quotes')
        user_category = data.get('user_category')
        user_language = data.get('user_language')
        

    # send quote
    await message.answer(trans('Запустилося✅\n По стандарту, буде відправляти кожні пів години одну цитату, можете змінити в налаштуваннях', dest=user_language).text)

    while True:
        data = await state.get_data()
        should_stop = data.get('should_stop', False)

        if should_stop:
            break

        random_num = random.randint(0, 3000)
        
        try:
            btns_add_favorite = [
                [types.InlineKeyboardButton(text=trans("Добавити в улюблені 📝").text, callback_data=f"add_favorite_{random_num}")]
            ]
            keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_add_favorite)

            quote = quotes[random_num]
            text = quote["text"]
            author = quote["author"]
            category = quote["category"]

            if user_category == "Всі":

                result = trans(f"{text}\n Автор - {author}\n Категорія - {category}").text

                await message.answer(result, reply_markup=keyboard_btns)
                await asyncio.sleep(user_time_quotes)

            elif user_category == category:

                result = trans(f"{text}\n Автор - {author}\n Категорія - {category}").text

                await message.answer(result, reply_markup=keyboard_btns)
                await asyncio.sleep(user_time_quotes)


        except IndexError:
            continue


@dp.message_handler(Text(equals=['Ручний режим', 'Manual mode']))
async def manual_mode(message: types.Message, state: FSMContext):

    # getting data user
    async with state.proxy() as data:
        data['should_stop'] = False   
        user_category = data.get('user_category')
        user_language = data.get('user_language')


    random_num = random.randint(0, 3000)


    btns_add_favorite = [
        [types.InlineKeyboardButton(text=trans("Добавити в улюблені 📝", dest=user_language).text, callback_data=f"add_favorite_{random_num}")]
    ]
    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_add_favorite)

    quote = quotes[random_num]
    text = quote["text"]
    author = quote["author"]
    category = quote["category"]


    if user_category == "Всі":

        result = trans(f"{text}\n Автор - {author}\n Категорія - {category}", dest=user_language).text
        await message.answer(result, reply_markup=keyboard_btns)

    elif user_category == category:

        result = trans(f"{text}\n Автор - {author}\n Категорія - {category}", dest=user_language).text
        await message.answer(result, reply_markup=keyboard_btns)


@dp.message_handler(Text(equals=['Зупинити ❌', 'Stop ❌']))
async def stop(message: types.Message, state: FSMContext):

    # save variable True, if user stopping loop 
    async with state.proxy() as data:
        data['should_stop'] = True
        user_language = data.get('user_language')


    await message.answer(trans('Зупинено ⏱❌', dest=user_language).text)
    

@dp.message_handler(Text(equals=['Назад ⏪', 'Back ⏪']))
async def btn_back(message: types.Message, state: FSMContext):

    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')


    # start buttons
    start_btns = [
        [types.KeyboardButton(text=trans('Запуск ✈', dest=user_language).text)],
        [types.KeyboardButton(text=trans('Налаштування ⚙', dest=user_language).text)],
        [types.KeyboardButton(text=trans('Мої улюблені цитати 📝💖', dest=user_language).text)],
        [types.KeyboardButton(text=trans("Зв'язок 💬", dest=user_language).text)],
        [types.KeyboardButton(text=trans('Зупинити ❌', dest=user_language).text)],
    ]
    keyboard_start_btns = types.ReplyKeyboardMarkup(keyboard=start_btns, resize_keyboard=True)


    await message.answer(trans('Головне меню', dest=user_language).text, reply_markup=keyboard_start_btns)