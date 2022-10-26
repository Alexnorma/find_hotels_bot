from dotenv import dotenv_values

config = dotenv_values(".env")
token = config['BOT_TOKEN']
api_key = config['RAPI_KEY']
