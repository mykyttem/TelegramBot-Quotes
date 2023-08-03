import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import firebase_admin
from firebase_admin import credentials, db

""" Bot """

API_TOKEN = 'your_token'


logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



""" fireBase """


cred = credentials.Certificate("file.json")
firebase_admin.initialize_app(cred, {"databaseURL": "your url"})

ref = db.reference('/')