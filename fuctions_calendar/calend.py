from loguru import logger
from telegram_bot_calendar import DetailedTelegramCalendar
import keyboards.inline
from base_functions import photos
from loader import bot
from states import MyStates


# ввод даты
@bot.message_handler(state=MyStates.check_in)
def get_date(callback_message):
    logger.info('Выбирается дата')
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(callback_message.message.chat.id, "Выберите дату", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal1(callback_message):
    result, key, step = DetailedTelegramCalendar(locale='ru').process(callback_message.data)
    cid = callback_message.message.chat.id
    cmid = callback_message.message.message_id
    if not result and key:
        if step == 'm':
            bot.edit_message_text('Выберите месяц', cid, cmid, reply_markup=key)
        elif step == 'y':
            bot.edit_message_text('Выберите год', cid, cmid, reply_markup=key)
        else:
            bot.edit_message_text('Выберите день', cid, cmid, reply_markup=key)
    elif result:
        logger.info(f'Дата result {result}')
        with bot.retrieve_data(
                callback_message.from_user.id,
                callback_message.message.chat.id) as data:
            if 'check_in' not in data.keys():
                data['check_in'] = result
                logger.info(f'Дата В bot.retrieve cal1 {data["check_in"]}')
            else:
                data['check_out'] = result
                logger.info(f'Дата {data["check_out"]}')
        confirmation(callback_message, result)


# обработка нажатия кнопок подтверждения даты
def confirmation(callback_message, result):
    logger.info(f'Дата result conf {result}')
    bot.edit_message_text(
        f"Вы выбрали {result} ?", callback_message.message.chat.id,
        callback_message.message.message_id,
        reply_markup=keyboards.inline.confirmation_buttons())


@bot.callback_query_handler(func=lambda mes: mes.data == "y")
def callback_yes_confirm(callback_message):

    with bot.retrieve_data(
            callback_message.from_user.id,
            callback_message.message.chat.id) as data:
        logger.info(f'c в ans {callback_message}')
        logger.info(f'data.keys в ans: {data.keys()}')
        if 'check_out' not in data.keys():
            logger.info('Дата въезда добавлена')
            bot.delete_message(
                callback_message.message.chat.id,
                callback_message.message.message_id)
            get_date(callback_message)
        else:
            logger.info('Дата выезда добавлена')
            bot.edit_message_text(
                "Дата записана",
                callback_message.message.chat.id,
                callback_message.message.message_id)
            photos.number_of_photos(callback_message)


@bot.callback_query_handler(func=lambda callback_message: callback_message.data == "n")
def callback_no_confirm(callback_message):
    with bot.retrieve_data(
            callback_message.from_user.id,
            callback_message.message.chat.id) as data:
        if 'check_out' not in data.keys():
            data.pop('check_in', 3000)
        else:
            data.pop('check_out', 3000)
    get_date(c.message)
    bot.delete_message(
        callback_message.message.chat.id,
        callback_message.message.message_id)
