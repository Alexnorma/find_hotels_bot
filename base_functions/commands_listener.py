from tg_commands import lowprice_tg, highprice_tg, history, bestdeal
from loader import bot
from states import MyStates

# Функция, обрабатывающая команду /highprice
def commands_listener(command):
    bot.set_state(command.from_user.id, MyStates.user, command.chat.id)
    if command.text == '/highprice':
        highprice_tg.send_highprice(command)
    elif command.text == '/lowprice':
        lowprice_tg.send_lowprice(command)
    elif command.text == '/bestdeal':
        bestdeal.send_bestdeal(command)
    elif command.text == '/history':
        history.send_history(command)
    elif command.text == '/helloworld':
        highprice_tg.send_welcome(command)

