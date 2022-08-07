from tg_commands import lowprice
import telebot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# Создаем экземпляр бота
token = "5338632260:AAHAnlfUFM-d21iYnMRTmJBolg9Y70hd3Bw"
bot = telebot.TeleBot(token)


# каледарь
# @bot.message_handler(commands=['calend'])
# def calend(m):
#     # do not forget to put calendar_id
#     calendar, step = DetailedTelegramCalendar(locale='ru').build()
#     if step == 'y':
#         LSTEP[step] = 'год'
#     bot.send_message(m.chat.id,
#                      f"Выберите {LSTEP[step]}",
#                      reply_markup=calendar)
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal1(c):
#     result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
#
#     if not result and key:
#         if step == 'm':
#             LSTEP[step] = 'месяц'
#         if step == 'd':
#             LSTEP[step] = 'день'
#         bot.edit_message_text(f"Выберите {LSTEP[step]}",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"Вы выбрали {lowprice.get_check_in_date(result)} ",
#                               c.message.chat.id,
#                               c.message.message_id)
#


# Функция, обрабатывающая команду /hello-world
@bot.message_handler(commands=['hello-world'])
def send_welcome(message):
    bot.reply_to(message, 'Это первое сообщение бота в ответ на команду hello_world ')


# Функция, обрабатывающая команду /lowprice
@bot.message_handler(commands=['lowprice'])
def send_lowprice(message):
    bot.send_message(message.from_user.id, "Введите город для поиска предложений:")
    bot.register_next_step_handler(message, get_answer)
def get_answer(message):
    list_data = lowprice.list_hotels_by_destination(message.text)
    print(list_data)
    print(type(list_data))
    bot.send_message(message.from_user.id, str(list_data))





    # list_hotels_by_destination('New York')





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