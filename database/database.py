from peewee import TextField, FloatField, \
    DateField, Model, TimeField, SqliteDatabase
from loguru import logger
from datetime import datetime

db = SqliteDatabase('database/history.db')


# таблица пользователей
class Users(Model):
    user_id = TextField()
    date = DateField()
    time = TimeField()
    command = TextField()
    city = TextField()
    check_in = TextField()
    check_out = TextField()
    suggestion = TextField()
    distance = FloatField()
    count_hotels = FloatField()
    count_photos = FloatField()

    class Meta:
        database = db


logger.info('Подключение к базе данных')
logger.catch()


def create_db():
    with db:
        db.create_tables([Users])
        logger.info('Таблица создана')
        return db


def add_query(suggestion, distance, data):
    logger.info(f'Таблица создана в add_query {data}')
    logger.info('Таблица создана в add_query')
    create_db()
    logger.info('Таблица создана в add_query')
    logger.info(data["user_id"])
    logger.info(datetime.now().date())
    logger.info(data['command'])
    logger.info(data['check_in'])
    logger.info(data['check_out'])
    logger.info(suggestion)
    logger.info(distance)
    new_user = Users.create(
        user_id=data['user_id'], date=datetime.now().date(), time=datetime.now().time(),
        command=data['command'], city=data['city'], check_in=data['check_in'],
        check_out=data['check_out'], suggestion=suggestion, distance=distance,
        count_photos=data['count_photos'], count_hotels=data['count_hotels'])
    return new_user


# получения истории пользователя
def get_history(id):
    logger.info('Запрос из базы данных')
    list_queries = []

    for i in Users.select().where(Users.user_id == id):
        logger.info('Формирование словаря c атрибутами ответа на запрос')
        list_data = dict()
        list_data['user_id'] = i.user_id
        list_data['date'] = i.date
        list_data['time'] = i.time
        list_data['command'] = i.command
        list_data['city'] = i.city
        list_data['check_in'] = i.check_in
        list_data['check_out'] = i.check_out
        list_data['suggestion'] = i.suggestion
        list_data['distance'] = i.distance
        list_data['count_photos'] = i.count_photos
        list_data['count_hotels'] = i.count_hotels
        list_queries.append(list_data)
        logger.info('Сформирован словарь c атрибутами ответа на запрос')
    return list_queries
