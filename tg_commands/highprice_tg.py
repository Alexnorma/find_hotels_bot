
def send_highprice(message, bot):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду highprice ')
# Функция, обрабатывающая команду /hello-world

def send_welcome(message,bot):
    bot.reply_to(message, 'Это первое сообщение бота в ответ на команду hello_world ')


# Функция, обрабатывающая команду /bestdeal

def send_bestdeal(message,bot):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду bestdeal')


# Функция, обрабатывающая команду /history

def send_history(message,bot):
    bot.reply_to(message, 'Это первое сообщеlние бота в ответ на команду history')

# Функция, обрабатывающая Привет
# @bot.message_handler(content_types=['text'])
# def send_hello(message):
#     if message.text == 'Привет':
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")