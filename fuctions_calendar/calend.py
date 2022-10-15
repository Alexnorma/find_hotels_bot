from loguru import logger
from telegram_bot_calendar import DetailedTelegramCalendar
from telebot import types

import keyboards.inline
from base_functions import photos
from loader import bot
from states import MyStates


# ввод даты
def get_date(message):

    logger.info('Выбирается дата')
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.set_state(message.from_user.id, MyStates.check_in, message.chat.id)
    bot.send_message(message.chat.id, f"Выберите дату", reply_markup=calendar)

    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def cal1(c):
        result, key, step = DetailedTelegramCalendar(locale='ru').process(c.data)
        cid = c.message.chat.id
        cmid = c.message.message_id
        if not result and key:
            if step == 'm':
                bot.edit_message_text('Выберите месяц', cid, cmid, reply_markup=key)
            elif step == 'y':
                bot.edit_message_text('Выберите год', cid, cmid, reply_markup=key)
            else:
                bot.edit_message_text('Выберите день', cid, cmid, reply_markup=key)
        elif result:
            logger.info(f'Дата result {result}')
            confirmation(c.message, result)

    # обработка нажатия кнопок подтверждения даты
    def confirmation(c, result):
        logger.info(f'Дата result conf {result}')
        cid = c.chat.id
        cmid = c.message_id
        bot.edit_message_text(f"Вы выбрали {result} ?", cid, cmid,
                              reply_markup=keyboards.inline.confirmation_buttons())
        ans(c, result)

    @bot.callback_query_handler(func=lambda mes: mes.data == "y")
    def ans(mes,result):
        logger.info(f'Дата ans(c): {result}')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if not 'check_in' in data.keys():
                data['check_in'] = result
                logger.info('Дата въезда добавлена')
                get_date(mes)
            else:
                data['check_out'] = result


                logger.info(f'Дата data["check_in"] {data["check_in"]}')
                logger.info(f'Дата data["check_out"] {data["check_out"]}')
                bot.edit_message_text("Дата записана", mes.chat.id, mes.message_id)
                photos.number_of_photos(message)


    @bot.callback_query_handler(func=lambda mes: mes.data == "n")
    def ansa(mes):
        get_date(mes.message)
        bot.delete_message(mes.chat.id,mes.message_id)





