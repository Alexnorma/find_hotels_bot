from loguru import logger
import keyboards.inline
from loader import bot
from states import MyStates
from base_functions import get_hotels


# получение количества показываемых в запросе фото
def number_of_photos(c):
    bot.set_state(c.from_user.id, MyStates.count_photos, c.message.chat.id)
    bot.send_message(c.message.chat.id,
                     "Сколько фото показывать?",
                     reply_markup=keyboards.inline.photos_buttons())
    logger.info('Ввод количества показываемых в запросе фото ')
    bot.register_next_step_handler(c.message, get_photos)


@bot.message_handler(state=MyStates.count_photos)
def get_photos(c):
    logger.info(f'c{c}')
    count = c.text
    with bot.retrieve_data(c.from_user.id, c.chat.id) as data:
        data['count_photos'] = count
    logger.info(count)
    logger.info(data.keys())
    get_hotels.get_num_hotels(c)
