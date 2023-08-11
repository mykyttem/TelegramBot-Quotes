from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import random
import asyncio

from config import dp, ref
from tools import l_trans, trans_google, quotes


#FIXME: if you do not start from the start, the user's language choice will not be found


""" Main functionals 
    Using "state: FSMContext" for pass variables between functions 
"""

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
        [types.KeyboardButton(text=l_trans('Запуск ✈', language))],
        [types.KeyboardButton(text=l_trans('Ручний режим', language))],
        [types.KeyboardButton(text=l_trans('Налаштування', language))],
        [types.KeyboardButton(text=l_trans('Мої улюблені цитати 📝💖', language))],
        [types.KeyboardButton(text=l_trans("Зв'язок 💬", language))],
        [types.KeyboardButton(text=l_trans('Зупинити ❌', language))],
    ]
    keyboard_start_btns = types.ReplyKeyboardMarkup(keyboard=start_btns, resize_keyboard=True)


    txt = l_trans("Привіт, це бот, якого задача мотивувати тебе В налаштуваннях можеш налаштувати систему сповіщень або інше", language)
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
    await message.answer(l_trans('Запустилося✅\n По стандарту, буде відправляти кожні пів години одну цитату, можете змінити в налаштуваннях', user_language))

    while True:
        data = await state.get_data()
        should_stop = data.get('should_stop', False)

        if should_stop:
            break

        random_num = random.randint(0, 3000)
        
        try:
            btns_add_favorite = [
                [types.InlineKeyboardButton(text=l_trans("Добавити в улюблені 📝", user_language), callback_data=f"add_favorite_{random_num}")]
            ]
            keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_add_favorite)

            quote = quotes[random_num]
            text = quote["text"]
            author = quote["author"]
            category = quote["category"]

            if user_category == "Всі":

                result = trans_google(f"{text}\n Автор - {author}\n Категорія - {category}", dest=user_language).text

                await message.answer(result, reply_markup=keyboard_btns)
                await asyncio.sleep(user_time_quotes)

            elif user_category == category:

                result = trans_google(f"{text}\n Автор - {author}\n Категорія - {category}", dest=user_language).text

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
        [types.InlineKeyboardButton(text=l_trans("Добавити в улюблені 📝", user_language), callback_data=f"add_favorite_{random_num}")]
    ]
    keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_add_favorite)

    quote = quotes[random_num]
    text = quote["text"]
    author = quote["author"]
    category = quote["category"]


    if user_category == "Всі":

        result = trans_google(f"{text}\n Автор - {author}\n Категорія - {category}", dest=user_language).text
        await message.answer(result, reply_markup=keyboard_btns)

    elif user_category == category:

        result = trans_google(f"{text}\n Автор - {author}\n Категорія - {category}", dest=user_language).text
        await message.answer(result, reply_markup=keyboard_btns)


@dp.message_handler(Text(equals=['Зупинити ❌', 'Stop ❌']))
async def stop(message: types.Message, state: FSMContext):

    # save variable True, if user stopping loop 
    async with state.proxy() as data:
        data['should_stop'] = True
        user_language = data.get('user_language')


    await message.answer(l_trans('Зупинено ⏱❌', user_language))
    

@dp.message_handler(Text(equals=['Назад ⏪', 'Back ⏪']))
async def btn_back(message: types.Message, state: FSMContext):

    # getting data user
    async with state.proxy() as data:
        user_language = data.get('user_language')


    # start buttons
    start_btns = [
        [types.KeyboardButton(text=l_trans('Запуск ✈', user_language))],
        [types.KeyboardButton(text=l_trans('Налаштування', user_language))],
        [types.KeyboardButton(text=l_trans('Мої улюблені цитати 📝💖', user_language))],
        [types.KeyboardButton(text=l_trans("Зв'язок 💬", user_language))],
        [types.KeyboardButton(text=l_trans('Зупинити ❌', user_language))],
    ]
    keyboard_start_btns = types.ReplyKeyboardMarkup(keyboard=start_btns, resize_keyboard=True)


    await message.answer(l_trans('Головне меню', user_language), reply_markup=keyboard_start_btns)  