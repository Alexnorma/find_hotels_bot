from loguru import logger
from loader import bot
from states import MyStates
from keyboards import inline
from tg_commands import lowprice_tg, bestdeal


# получение количества отелей для показа
def get_num_hotels(message):
    logger.info('Получение количества отелей для показа ')
    bot.set_state(message.from_user.id, MyStates.count_hotels, message.chat.id)
    bot.send_message(
        message.chat.id,
        "Сколько отелей показывать при выводе?(не более 25)",
        reply_markup=inline.hotels_buttons())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['command'] == '/lowprice':
            bot.register_next_step_handler(
                message, lowprice_tg.get_suggestions)
        elif data['command'] == '/bestdeal':
            bot.register_next_step_handler(message, bestdeal.start_of_price)
