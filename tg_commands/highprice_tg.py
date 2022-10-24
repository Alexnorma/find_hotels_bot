# Функция, обрабатывающая команду /highprice
from telebot import types
from loguru import logger
from base_functions import site_functions
from database import database
from fuctions_calendar import calend
from base_functions import get_hotels
from keyboards import inline
from loader import bot, sticker_id
from states import MyStates


# Функция, обрабатывающая команду /send_highprice
@logger.catch()
def send_highprice(message):
    logger.info('Запуск команды send_highprice')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_id'] = message.from_user.id
        data['command'] = message.text
    logger.info('Добавлены user_id и command в data пользователя ')
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.from_user.id,
                     "Введите город для поиска предложений:")
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(state=MyStates.city)
def get_city(message):
    logger.info('Получение названий для кнопок выбора ')
    destinations = inline.city_markup_buttons(message.text)
    if destinations:
        logger.info('Названия получены ')
        bot.send_message(message.from_user.id,
                         'Уточните, пожалуйста:',
                         reply_markup=destinations)
        logger.info('Отправили кнопки в чат ')
    # Отправляем кнопки с вариантами
    else:
        logger.info('Нет такого города')
        bot.send_message(message.from_user.id,
                         "Нет такого города,введите ещё раз:")
        send_highprice(message)


@bot.callback_query_handler(func=lambda c: c.data.startswith("city"))
def callback_name_of_city(callback_message):
    logger.info('пользователь уточнил название')
    logger.info('Добавляем город в запрос для поиска')
    city = callback_message.data.split(',')[1]
    city_id = callback_message.data.split(',')[2]
    logger.info('получили ид и город')
    with bot.retrieve_data(
            callback_message.from_user.id,
            callback_message.message.chat.id) as data:
        data['city'] = city
        data['city_id'] = city_id
        logger.info('Добавлены city и city_id в data пользователя ')
    bot.edit_message_text(
        f"Вы выбрали {city}",
        callback_message.message.chat.id,
        callback_message.message.message_id)
    if callback_message.data:
        calend.get_date(callback_message)


@bot.message_handler(state=MyStates.count_hotels)
def get_suggestions(message):
    num_hotels = message.text
    if not 0 < int(message.text) <= 25:
        bot.send_message(
            message.chat.id,
            f"Вы ввели число {num_hotels},введите число не более 25")
        get_hotels.get_num_hotels(message)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['sortOrder'] = 'PRICE_HIGHEST_FIRST'
        data['distance'] = '1000'
        data['count_hotels'] = num_hotels
        logger.info('Добавлены sortOrder, distance, count_hotels в data пользователя')
    stiker = bot.send_sticker(message.chat.id, sticker=sticker_id)
    suggestions, distances = site_functions.list_hotels_by_destination(message)
    logger.info('suggestions n distance получили')
    list_photos = []
    logger.info('Отправка подобранных вариантов в чат')
    bot.delete_message(message.chat.id, stiker.message_id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        for k in range(0, int(num_hotels)):
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



