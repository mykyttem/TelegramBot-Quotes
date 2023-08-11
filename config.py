import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import firebase_admin
from firebase_admin import credentials, db

""" Bot """

API_TOKEN = '6119096459:AAHs7sc7jpotTyuwqdfb1gaU0_2QNwGqxAs'


logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



""" fireBase """


cred = credentials.Certificate("telegrambot-quotes-firebase-adminsdk-z5ze0-e4cb508be3.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://telegrambot-quotes-default-rtdb.firebaseio.com/"})

ref = db.reference('/')