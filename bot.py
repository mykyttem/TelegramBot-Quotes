from aiogram import executor
from aiogram import types

from config import dp


# beginning
@dp.message_handler(commands=['start'])
async def choice_languages(message: types.Message):

    # start buttons
    start_btns = [
        [types.KeyboardButton(text='Info')],
    ]

    keyboard_btns = types.ReplyKeyboardMarkup(keyboard=start_btns, resize_keyboard=True)

    await message.answer('Привіт', reply_markup=keyboard_btns)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)