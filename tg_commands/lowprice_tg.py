import requests
from telebot import types
from tg_commands import site_functions
from telegram_bot_calendar import DetailedTelegramCalendar
from loguru import logger
#данные запроса
data_query = {}


# Функция, обрабатывающая команду /lowprice
@logger.catch()
def send_lowprice(message, bot):
    logger.info('Запуск команды lowprice')
    bot.send_message(message.from_user.id, "Введите город для поиска предложений:")
    bot.register_next_step_handler(message, get_city, bot)


def get_city(message, bot):
    logger.info('Получение расположения')
    list_data = site_functions.get_distination(message.text)
    logger.info('Получили список мест для уточнения')
    #list_data = {'New York': '12345'}

    markup_city = types.InlineKeyboardMarkup()
    list_buttons = []
    for item in list_data.keys():
        list_buttons.append(types.InlineKeyboardButton(f'{item}', callback_data=f"city,{item}"))
    for button in list_buttons:
        markup_city .row(button)
    bot.send_message(message.chat.id, "Уточните адрес", reply_markup=markup_city)



    @bot.callback_query_handler(func=lambda c: c.data.startswith("city"))
    def ans(c):
        logger.info('Добавляем город в запрос для поиска')
        city = c.data.split(',')[1]
        data_query['city'] = city
        data_query['id'] = list_data[city]
        bot.edit_message_text(f"Вы выбрали {city}", c.message.chat.id, c.message.message_id)
        if c.data:
            get_date(message, bot)  # узнаем даты


# ввод даты
def get_date(message, bot):
    logger.info('Выбирается дата')
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    if len(data_query) < 2:
        bot.send_message(message.chat.id, "Выберите дату заезда", reply_markup=calendar)
    else:
        bot.send_message(message.chat.id, "Выберите дату выезда", reply_markup=calendar)


    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def cal1(c):
        result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
        cid = c.message.chat.id
        cmid = c.message.message_id
        if not result and key:
            if step == 'm':
                bot.edit_message_text('Выберите месяц', cid, cmid, reply_markup=key)
            elif step == 'y':
                bot.edit_message_text('Выберите год', cid, cmid, reply_markup=key)
            else:
                bot.edit_message_text('Выберите день', cid, cmid, reply_markup=key)
        elif result:
            confirmation(cid, cmid, result, bot)


# обработка нажатия кнопок подтверждения даты
def confirmation(cid, cmid, result, bot):
    markup = types.InlineKeyboardMarkup()
    button_a = types.InlineKeyboardButton('ДА', callback_data='y')
    button_b= types.InlineKeyboardButton('НЕТ', callback_data='n')
    markup.row(button_a, button_b)
    bot.edit_message_text(f"Вы выбрали {result} ?", cid, cmid, reply_markup=markup)

    @bot.callback_query_handler(func=lambda c: c.data == "y")
    def ans(c):
        if not 'check_in' in data_query.keys():
            data_query['check_in'] = result
            logger.info('Дата въезда добавлена')
        else:
            data_query['check_out'] = result
            logger.info('Дата выезда добавлена')
        bot.edit_message_text("Дата записана", c.message.chat.id, c.message.message_id)
        if len(data_query) < 4:
            get_date(c.message, bot)
        if len(data_query) == 4:
            number_of_photos(c, bot)


    @bot.callback_query_handler(func=lambda c: c.data == "n")
    def ansa(c):
        get_date(c.message, bot)
        bot.delete_message(cid, cmid)


# получение количества показываемых в запросе фото
def number_of_photos(c, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    one = types.KeyboardButton(text='1')
    three = types.KeyboardButton(text='3')
    five = types.KeyboardButton(text='5')
    markup.row(one, three, five)
    bot.send_message(c.message.chat.id, "Сколько фото показывать?", reply_markup=markup)
    logger.info('Ввод количества показываемых в запросе фото ')
    bot.register_next_step_handler(c.message, get_photos, bot)


def get_photos(message, bot):

    data_query['count_photos'] = message.text
    bot.send_message(message.chat.id,'записано')
    get_num_hotels(message, bot)



# получение количества отелей для показа
def get_num_hotels(message, bot):
    logger.info('Получение количества отелей для показа ')
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    b_1 = types.KeyboardButton(text='5')
    b_2 = types.KeyboardButton(text='7')
    b_3 = types.KeyboardButton(text='10')
    b_4 = types.KeyboardButton(text='15')
    b_5 = types.KeyboardButton(text='20')
    b_6 = types.KeyboardButton(text='25')
    markup.row(b_1,b_2,b_3,b_4,b_5,b_6)
    bot.send_message(message.chat.id, "Сколько отелей показывать при выводе?(не более 25)", reply_markup=markup)
    bot.register_next_step_handler(message, get_suggestions, bot, data_query)



def get_suggestions(message, bot, data_query):
    num_hotels = message.text
    if not 0 < int(message.text) <= 25:
        bot.send_message(message.chat.id, f"Вы ввели число {num_hotels},введите число не более 25")
        get_num_hotels(message, bot)
    data_query['sortOrder'] = 'PRICE'
    data_query
    suggestions = site_functions.list_hotels_by_destination(data_query)
    list_photos = []
    logger.info('Отправка подобранных вариантов в чат')
    for k in range(0, int(num_hotels)):
        if k > len(suggestions)-1:
            bot.send_message(message.chat.id, "Показаны все найденные результаты")
            break
        detail = site_functions.get_details(suggestions[k], data_query['check_in'], data_query['check_out'])
        res = site_functions.process_photos(suggestions[k], data_query['count_photos'])
        for i in res:
            list_photos.append(types.InputMediaPhoto(i))
        list_photos[0].caption = detail
        bot.send_media_group(message.chat.id, list_photos)
        list_photos.clear()











