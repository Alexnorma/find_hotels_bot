from telebot import types
from loguru import logger
from base_functions import site_functions
from database import database
from fuctions_calendar import calend
from base_functions import get_hotels
from keyboards import inline
from loader import bot
from states import MyStates


# Функция, обрабатывающая команду /bestdeal
@logger.catch()
@bot.message_handler(state=MyStates.user)
def send_bestdeal(message):
    logger.info('Запуск команды lowprice')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id
        data['command'] = message.text
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     "Введите город для поиска предложений:")
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(state=MyStates.city)
def get_city(message):
    destinations = inline.city_markup(message.text)
    if destinations:
        # Отправляем кнопки с вариантами
        bot.send_message(message.from_user.id, 'Уточните, пожалуйста:',
                         reply_markup=destinations)
    else:
        logger.info('Нет такого города')
        bot.send_message(message.from_user.id,
                         "Нет такого города,введите ещё раз:")
        send_bestdeal(message)

@bot.callback_query_handler(func=lambda c: c.data.startswith("city"))
def ans(c):
    logger.info(f'c data {c}')
    logger.info('Добавляем город в запрос для поиска')
    city = c.data.split(',')[1]
    city_id = c.data.split(',')[2]
    logger.info('получили ид и город')
    with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
        data['city'] = city
        data['city_id'] = city_id
        logger.info(data.keys())
    bot.edit_message_text(
        f"Вы выбрали {city}",
        c.message.chat.id, c.message.message_id)
    if c.data:
        calend.get_date(c)


# ввод диапазона цен(начальная цена)
@bot.message_handler(state=MyStates.count_hotels)
def start_price(message):
    num_hotels = message.text
    if not 0 < int(message.text) <= 25:
        bot.send_message(
            message.chat.id,
            f"Вы ввели число {num_hotels},введите число не более 25")
        get_hotels.get_num_hotels(message)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_hotels'] = num_hotels
    logger.info('Ввод начальной цены')
    bot.send_message(message.chat.id, "начальная цена?",
                     reply_markup=inline.start_price_buttons())
    bot.register_next_step_handler(message, end_price)


# ввод диапазона цен(конечная цена)
def end_price(message):
    logger.info('Ввод конечной цены')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['start_price'] = message.text

    bot.send_message(message.chat.id, "конечная цена?",
                     reply_markup=inline.end_price_buttons())
    bot.register_next_step_handler(message, dist_center)


# ввод расстояния от центра
def dist_center(message):
    logger.info('Ввод расстояния от центра')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['end_price'] = message.text
    bot.send_message(message.chat.id, "Расстояние от центра?")
    bot.register_next_step_handler(message, get_suggestions)


# вывод предложений
@logger.catch()
def get_suggestions(message):
    distance = message.text
    if not 0 < int(message.text) <= 1000:
        bot.send_message(
            message.chat.id,
            f"Вы ввели число {distance},введите число от 0 до 1000")
        dist_center(message)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sortOrder'] = 'DISTANCE'
        data['distance'] = distance
    logger.info(data.keys())
    logger.info(data.items())
    suggestions, distances = site_functions.list_hotels_by_destination(message)
    logger.info(f'suggestions {suggestions}')
    logger.info(f'distance {distances}')
    list_photos = []
    logger.info('Отправка подобранных вариантов в чат')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for k in range(0, int(data['count_hotels'])):
            if k > len(suggestions) - 1:
                bot.send_message(message.chat.id,
                                 "Показаны все найденные результаты")
                break
            else:
                database.add_query(suggestions[k], distances[k], data)
                detail = site_functions.get_details(
                    suggestions[k], data['check_in'],
                    data['check_out'], distances[k])
                res = site_functions.process_photos(
                    suggestions[k], data['count_photos'])
                for i in res:
                    list_photos.append(types.InputMediaPhoto(i))
                list_photos[0].caption = detail
                bot.send_media_group(message.chat.id, list_photos)
                logger.info('Результат отправлен в чат')
                list_photos.clear()
