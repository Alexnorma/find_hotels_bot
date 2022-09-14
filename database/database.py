from peewee import *
from loguru import logger
from datetime import datetime


db = SqliteDatabase('database\history.db')


#таблица пользователей
class Users(Model):

    user_id = TextField()
    date = TextField()
    command = TextField()
    city = TextField()
    check_in = TextField()
    check_out = TextField()

    class Meta:
        database = db


logger.info('Подключение к базе данных')
logger.catch()


def create_db():
    with db:
        db.create_tables([Users])
        logger.info('Таблица создана')
        return db


def add_query(data_query):
    logger.info('Запись добавлена в базу данных')
    new_user = Users.create(user_id=data_query['user_id'], date=datetime.now().date(), command=data_query['command']
                            , city=data_query['city'], check_in=data_query['check_in']
                            , check_out=data_query['check_out'])
    return new_user


#получения истории пользователя
def get_history(id):
    logger.info('Запрос из базы данных')
    records = Users.select().where(Users.user_id == id)
    count_records = len(records)

    list_queries = []
    for i in Users.select().where(Users.user_id == id):
        list_data = dict()
        list_data['user_id'] = i.user_id
        list_data['command'] = i.command
        list_data['city'] = i.city
        list_data['check_in'] = i.check_in
        list_data['check_out'] = i.check_out
        list_queries.append(list_data)
    return list_queries
















