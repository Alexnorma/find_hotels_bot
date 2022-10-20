from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.token, state_storage=storage)
api_key = config.api_key
api_host = "hotels4.p.rapidapi.com"
