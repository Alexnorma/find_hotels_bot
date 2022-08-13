from tg_commands import lowprice
import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# Создаем экземпляр бота
token = "5338632260:AAHAnlfUFM-d21iYnMRTmJBolg9Y70hd3Bw"
bot = telebot.TeleBot(token)

data_query = {}#данные запроса


def get_suggestions(data_query):
    suggestions = lowprice.list_hotels_by_destination(data_query)
    return suggestions


# def post_results()->str:
#
#     suggestions = get_suggestions(data_query)
#     for mes in suggestions:
#          mes = lowprice.get_details(mes, check_in=data_query[3], check_out=data_query[4])
#     #    bot.send_message(message,mes)
#     return '123'




# Функция, обрабатывающая команду /hello-world
@bot.message_handler(commands=['hello-world'])
def send_welcome(message):
    bot.reply_to(message, 'Это первое сообщение бота в ответ на команду hello_world ')


# Функция, обрабатывающая команду /lowprice
@bot.message_handler(commands=['lowprice'])
def send_lowprice(message):
    bot.send_message(message.from_user.id, "Введите город для поиска предложений:")
    bot.register_next_step_handler(message, get_city)


def get_city(message):
    list_data = lowprice.get_distination(message.text)
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
        city = c.data.split(',')[1]
        data_query['city'] = city
        data_query['id'] = list_data[city]
        bot.edit_message_text(f"Вы выбрали {city}", c.message.chat.id, c.message.message_id)
        if c.data:
            get_date(message)  # узнаем даты


def get_date(message):
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    if len(data_query) < 2:
        bot.send_message(message.chat.id, f"Выберите дату заезда", reply_markup=calendar)
    else:
        bot.send_message(message.chat.id, f"Выберите дату выезда", reply_markup=calendar)


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
        confirmation(cid, cmid, result)


        # обработка нажатия кнопок ответа


def confirmation(cid, cmid, result):
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
            get_date(c.message)
        if len(data_query) == 4:
            suggestions = get_suggestions(data_query)
            print(suggestions)
            for mes in suggestions:

                mes = lowprice.get_details(mes)
                bot.send_message(c.message.chat.id, str(mes))


    @bot.callback_query_handler(func=lambda c: c.data == "n")
    def ansa(c):
        get_date(c.message)
        bot.delete_message(cid, cmid)



# Функция, обрабатывающая команду /highprice
@bot.message_handler(commands=['highprice'])
def send_highprice(message):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду highprice ')


# Функция, обрабатывающая команду /bestdeal
@bot.message_handler(commands=['bestdeal'])
def send_bestdeal(message):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду bestdeal')


# Функция, обрабатывающая команду /history
@bot.message_handler(commands=['history'])
def send_history(message):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду history')

# Функция, обрабатывающая Привет
@bot.message_handler(content_types=['text'])
def send_hello(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")


# Запускаем бота

bot.polling(none_stop=True, interval=0)