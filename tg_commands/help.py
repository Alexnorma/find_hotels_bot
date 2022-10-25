from loader import bot
from loguru import logger


# Функция, обрабатывающая команду /help
def send_help(message):
    bot.send_message(message.from_user.id,
                 f'Приветcтвую Вас {message.from_user.first_name}!\nВот что может этот бот: \n'
                 f'/help - помощь по камандам бота \n'
                 f'/lowprice  - поиск номеров по низким ценам \n'
                 f'/highprice  - поиск номеров по высоким ценам \n'
                 f'/bestdeal  - поиск номеров по лучшей цене \n'
                 f'/history - история поиска')