from database import database
from loader import bot
from base_functions import site_functions
from telebot import types
from loguru import logger


# Функция, обрабатывающая команду /history
def send_history(message):
    data = database.get_history(message.from_user.id)
    print(data)
    for i in data:
        command = i['command']
        # city = i['city']
        check_out = i['check_out']
        check_in = i['check_in']
        count_photos = i['count_photos']
        # num_hotels = i['count_hotels']
        suggestion = i['suggestion']
        distance = i['distance']
        list_photos = []
        detail = site_functions.get_details(suggestion,
                                            check_in, check_out, distance)
        res = site_functions.process_photos(suggestion, count_photos)
        for i in res:
            list_photos.append(types.InputMediaPhoto(i))
        list_photos[0].caption = f'{detail}\n Команда: {command}'
        bot.send_media_group(message.chat.id, list_photos)
        logger.info('Результат отправлен в чат')
        list_photos.clear()
    logger.info('Все результатц отправлены')
    bot.send_message(message.chat.id, "Показаны все найденные результаты")
