from aiogram import types
from aiogram.dispatcher.filters import Text

from config import dp, ref
from start_bot import quotes


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