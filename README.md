Бот написан на Python 3.9. Для работы бота необходимо дополнительно установить библиотеки «Requests» и «pyTelegramBotAPI» 
Бот использует API "rapidapi.com". Для работы с БД используется sqlite3. 

Состав: Бот состоит из следующих модулей:

«config.py» – содержит конфигурационные настройки, такие как API key, token для telegram бота и остальные настройки.
«database.py» - содержит процедуры для работы с БД.
«main.py» - Основной модуль. Содержит процедуры для анализа ответов пользователя и вывода результатов в чат.
«site_functions.py» - модуль для работы c API
«history.db» - файл базы данных, необязателен.
Начало работы: Для запуска бота необходим установленный интерпретатор Python версии 3.9 все остальные пакеты в requirements.txt.
Нужен файл .env куда нужно сохранить RAPIDAPI_KEY и токен от вашего бота. 