import telebot #telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    user = State()
    city = State()
    check_in = State()
    count_photos = State()
    count_hotels = State()
    parametrs = State()


