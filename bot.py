from aiogram import executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import random
import asyncio
import os
import json

from config import dp, ref, bot


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
            {"id": id_user, "time-quotes": 1800, "favorite": [0], "category": "all"}
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
    


""" My favorites """

@dp.callback_query_handler(lambda c: c.data.startswith('add_favorite_'))
async def add_favorite(callback_query: types.CallbackQuery):
    await callback_query.answer()

    # Convert num_quote to an integer
    num_quote = int(callback_query.data.split('_')[2])

    # Getting user data
    username = callback_query.from_user.username
    user_data = ref.child(username).get()
    user_list_favorite = user_data.get("favorite", [])

    # Append the new favorite to the list
    user_list_favorite.append(num_quote)

    # Update the "favorite" field in the user_data
    user_data["favorite"] = user_list_favorite

    # Save the updated user_data in the database
    ref.child(username).update(user_data)

    await callback_query.message.answer('Успішно добавленно 📝✅') 


@dp.message_handler(Text(equals=['Мої улюблені цитати 📝💖']))
async def my_favorite(message: types.Message):
    
    # data user, getting list favorites quotes
    username = message.from_user.username
    user_data = ref.child(username).get()
    user_list_favorite = user_data.get("favorite")

    if user_list_favorite:

        for num in user_list_favorite:

            btns_delete_favorite = [
                [types.InlineKeyboardButton(text="Видалити з улюблених ❌", callback_data=f"delete_favorite_{num}")]
            ]
            keyboard_btns = types.InlineKeyboardMarkup(inline_keyboard=btns_delete_favorite)


            quote = quotes[num]
            text = quote["text"]
            author = quote["author"]
            category = quote["category"]


            result = f"{text}\n Автор - {author}\n Категорія - {category}"
            await message.answer(result, reply_markup=keyboard_btns)
    
    else:
        await message.answer("Ви нічого не добавили 😕")


@dp.callback_query_handler(lambda c: c.data.startswith('delete_favorite_'))
async def delete_favorite(callback_query: types.CallbackQuery):
    await callback_query.answer()

    num_quote = int(callback_query.data.split('_')[2])

    # data user, getting list favorites quotes
    username = callback_query.from_user.username
    user_data = ref.child(username).get()
    user_list_favorite = user_data.get("favorite", [])

    # delete quote
    user_list_favorite.remove(num_quote)

    # Update the "favorite" field in the user_data
    user_data["favorite"] = user_list_favorite

    # Save the updated user_data in the database
    ref.child(username).update(user_data)    
    await callback_query.message.answer('Видалено 🗑✅')


@dp.message_handler(Text(equals=['Назад ⏪']))
async def btn_back(message: types.Message):
    await message.answer('Головне меню', reply_markup=keyboard_start_btns)


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



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)