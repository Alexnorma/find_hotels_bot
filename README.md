## О боте:

Бот используется для поиска предложений и бронирования номеров в отелях.
Работа бота осуществляется с сайтом Hotels.com

Бот написан на языке Python и использует API "rapidapi.com". Для работы с БД используется sqlite3. 
Дополнительно требуется установка библиотек «Requests» и «pyTelegramBotAPI»

## Команды бота:
* lowprice  - поиск номеров по низким ценам
* highprice - поиск номеров по высоким ценам
* bestdeal - поиск номеров по лучшей цене
* history - история поиска
* help - помощь по камандам бота

### lowprice
После ввода команды у пользователя запрашивается:
1. Город, где будет провоодиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Результаты сортируются начиная от самой низкой цены

### highprice
После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Результаты сортируются начиная от самой высокой цены

### bestdeal
После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Результаты сортируются по цене и расположению от центра.

### history
Ввод отелей которые ранее были найдены при поиске

## Бот состоит из следующих модулей:

* «config.py» – содержит конфигурационные настройки, такие как API key, token для telegram бота и остальные настройки.
* «database.py» - содержит процедуры для работы с БД.
* «main.py» - Основной модуль. Содержит процедуры для анализа ответов пользователя и вывода результатов в чат.
* «site_functions.py» - модуль для работы c API
* «history.db» - файл базы данных, необязателен.

## Начало работы с ботом

Загрузка бота с GIT через SSH:
> git clone git@gitlab.skillbox.ru:aleksandr_shamshurin/python_basic_diploma_non-profile.git

Загрузка бота с GIT через HTTPS:

>git clone https://gitlab.skillbox.ru/aleksandr_shamshurin/python_basic_diploma_non-profile.git

Создайте файл .env в корне проекта и укажите токен бота и ключ для API в формате:
>BOT_TOKEN = "здесь токен"
>RAPI_KEY = "здесь ключ API"

Установите Python версии 3.9 и все остальные пакеты указанные в requirements.txt.


