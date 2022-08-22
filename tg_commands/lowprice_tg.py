import requests
from telebot import types
from tg_commands import lowprice_site
from telegram_bot_calendar import DetailedTelegramCalendar
#данные запроса
data_query = {}


# Функция, обрабатывающая команду /lowprice
def send_lowprice(message, bot):
    bot.send_message(message.from_user.id, "Введите город для поиска предложений:")
    bot.register_next_step_handler(message, get_city, bot)


def get_city(message, bot):
    list_data = lowprice_site.get_distination(message.text)
    # list_data = {'New York': '12345'}

    markup_city = types.InlineKeyboardMarkup()
    list_buttons = []
    for item in list_data.keys():
        list_buttons.append(types.InlineKeyboardButton(f'{item}', callback_data=f"city,{item}"))
    for button in list_buttons:
        markup_city .row(button)
    bot.send_message(message.chat.id, "Уточните адрес", reply_markup=markup_city)



    @bot.callback_query_handler(func=lambda c: c.data.startswith("city"))
    def ans(c):
        city = c.data.split(',')[1]
        data_query['city'] = city
        data_query['id'] = list_data[city]
        bot.edit_message_text(f"Вы выбрали {city}", c.message.chat.id, c.message.message_id)
        if c.data:
            get_date(message, bot)  # узнаем даты

# ввод даты


def get_date(message, bot):
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
        else:
            data_query['check_out'] = result
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
    bot.register_next_step_handler(c.message, get_photos, bot)


def get_photos(message, bot):

    data_query['count_photos'] = message.text

    bot.send_message(message.chat.id,'записано')
    get_suggestions(message.chat.id, bot, data_query)


def get_suggestions(message, bot, data_query):
    suggestions = lowprice_site.list_hotels_by_destination(data_query)
    list_photos = []
    for k in suggestions:
        detail = lowprice_site.get_details(k)
        res = lowprice_site.process_photos(k, data_query['count_photos'])
        for i in res:
            list_photos.append(types.InputMediaPhoto(i))
        list_photos[0].caption = detail
        bot.send_media_group(message, list_photos)
        list_photos.clear()









