from loguru import logger
from telebot import types
from base_functions import site_functions


def city_markup(message):
    logger.info('Получение расположения')
    cities = site_functions.get_distination(message)
    logger.info('Получили список мест для уточнения')
    # Функция "cget_distination" уже возвращает список словарей с нужным именем и id
    destinations = types.InlineKeyboardMarkup()
    if not cities:
        destinations = False
        return destinations
    else:
        for city in cities.keys():
            destinations.add(types.InlineKeyboardButton(text=f'{city}',
                                                        callback_data=f'city,{city},{cities[city]}'))
        return destinations


def confirmation_buttons():

    markup = types.InlineKeyboardMarkup()
    button_a = types.InlineKeyboardButton('ДА', callback_data='y')
    button_b = types.InlineKeyboardButton('НЕТ', callback_data='n')
    markup.row(button_a, button_b)
    return markup


def photos_buttons():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    one = types.KeyboardButton(text='1')
    three = types.KeyboardButton(text='3')
    five = types.KeyboardButton(text='5')
    markup.row(one, three, five)
    return markup


def hotels_buttons():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    b_1 = types.KeyboardButton(text='5')
    b_2 = types.KeyboardButton(text='7')
    b_3 = types.KeyboardButton(text='10')
    b_4 = types.KeyboardButton(text='15')
    b_5 = types.KeyboardButton(text='20')
    b_6 = types.KeyboardButton(text='25')
    markup.row(b_1, b_2, b_3, b_4, b_5, b_6)
    return markup


def start_price_buttons():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    b_1 = types.KeyboardButton(text='50')
    b_2 = types.KeyboardButton(text='100')
    b_3 = types.KeyboardButton(text='300')
    b_4 = types.KeyboardButton(text='300')
    markup.row(b_1, b_2, b_3, b_4)
    return markup
def end_price_buttons():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    b_1 = types.KeyboardButton(text='1000')
    b_2 = types.KeyboardButton(text='2000')
    b_3 = types.KeyboardButton(text='5000')
    b_4 = types.KeyboardButton(text='10000')
    markup.row(b_1, b_2, b_3, b_4)
    return markup



