from tg_commands import lowprice
import telebot


# Создаем экземпляр бота
token = "5338632260:AAHAnlfUFM-d21iYnMRTmJBolg9Y70hd3Bw"
bot = telebot.TeleBot(token)


# Функция, обрабатывающая команду /hello-world
@bot.message_handler(commands=['hello-world'])
def send_welcome(message):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду hello_world ')


# Функция, обрабатывающая команду /lowprice
@bot.message_handler(commands=['lowprice'])
def send_welcome(message):
    list_hotels= lowprice.list_hotels_by_destination('New York')
    bot.reply_to(message, f'Это первое сообщеlние бота в ответ на команду {list_hotels}')


# Функция, обрабатывающая команду /highprice
@bot.message_handler(commands=['highprice'])
def send_welcome(message):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду highprice ')


# Функция, обрабатывающая команду /bestdeal
@bot.message_handler(commands=['bestdeal'])
def send_welcome(message):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду bestdeal')


# Функция, обрабатывающая команду /history
@bot.message_handler(commands=['history'])
def send_welcome(message):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду history')

# Функция, обрабатывающая Привет
@bot.message_handler(content_types=['text'])
def send_hellu(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")


# Запускаем бота

bot.polling(none_stop=True, interval=0)