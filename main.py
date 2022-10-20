from base_functions import commands_listener
from loader import bot


# функция реагирующая на сообщения и команды
def handle_commands(commands):
    for command in commands:
        commands_listener.commands_listener(command)
# Запускаем бота


bot.set_update_listener(handle_commands)
bot.infinity_polling()
