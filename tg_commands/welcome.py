from loader import bot


# Функция, обрабатывающая команду /hello-world
def send_welcome(message):
    bot.reply_to(message,
                 'Это первое сообщение бота в ответ на команду hello_world ')