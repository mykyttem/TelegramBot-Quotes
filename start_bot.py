from aiogram import executor

from config import dp

from bot.main_functionals import *
from bot.my_favorites import *
from bot.communication import *
from bot.settings import *


""" Main file for start bot """


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)