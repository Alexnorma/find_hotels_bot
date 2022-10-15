from loguru import logger
import keyboards.inline
from loader import bot
from states import MyStates
from base_functions import get_hotels


# получение количества показываемых в запросе фото
def number_of_photos(message):
    bot.set_state(message.from_user.id, MyStates.count_photos, message.chat.id)
    bot.send_message(message.chat.id, "Сколько фото показывать?", reply_markup=keyboards.inline.photos_buttons())
    logger.info('Ввод количества показываемых в запросе фото ')

    bot.register_next_step_handler(message, get_photos)


@bot.message_handler(state=MyStates.count_photos)
def get_photos(message):
    count = message.text
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['count_photos'] = count
    logger.info(count)
    logger.info(data.keys())
    get_hotels.get_num_hotels(message)





