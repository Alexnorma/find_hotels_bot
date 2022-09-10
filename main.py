import telebot
from dotenv import dotenv_values
from tg_commands import commands_listener

# Создаем экземпляр бота
config = dotenv_values(".env")
token = config['BOT_TOKEN']
bot = telebot.TeleBot(token)


# функция реагирующая на сообщения и команды
def handle_commands(commands):

    for command in commands:
        commands_listener.commands_listener(command, bot)


# Запускаем бота


bot.set_update_listener(handle_commands)
bot.infinity_polling()





