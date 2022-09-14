from database import database


# Функция, обрабатывающая команду /history
def send_history(message,bot):

    data = database.get_history(message.from_user.id)
    print(data)
    for i in data:
        answer_query = 'Команда: {command}\nГород: {city}\nДата въезда: {check_in}\nДата выезда{check_out} '.format(city=i['city']
                                                                  , command=i['command']
                                           ,check_in=i['check_in'],check_out=i['check_out'])
        bot.send_message(message.from_user.id, answer_query)

