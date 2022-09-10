from tg_commands import lowprice_tg, highprice_tg,history,bestdeal


# Функция, обрабатывающая команду /highprice
def commands_listener(command, bot):
    if command.text == '/highprice':
        highprice_tg.send_highprice(command, bot)
    elif command.text == '/lowprice':
        lowprice_tg.send_lowprice(command, bot)
    elif command.text == '/bestdeal':
        bestdeal.send_bestdeal(command, bot)
    elif command.text == '/history':
        history.send_history(command, bot)
    elif command.text == '/helloworld':
        highprice_tg.send_welcome(command, bot)

