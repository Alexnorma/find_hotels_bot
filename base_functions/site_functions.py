import json
import requests
import re
from loguru import logger
from loader import bot
from loader import api_key, api_host


#получение фото
@logger.catch()
def get_photos(id: str) -> dict:

	url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
	querystring = {"id": id}
	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": api_host
	}
	logger.info('Отправка запроса для получения фото')
	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	return result


#обработка фоток
def process_photos(id: str, count_photos: str) -> list:
	logger.info('Обработка фото')
	all_photo = get_photos(id)
	try:
		data_photos = all_photo['hotelImages']
		pattern = r'{size}'
		list_photos = [data_photos[i]['baseUrl'] for i in range(0, int(count_photos))]
		resize_photos = [re.sub(pattern, 'z', item) for item in list_photos]
		return resize_photos
	except Exception:
		logger.info('список с ид фото пуст')




#получение конкретного места для поиска номеров
def get_distination(city: str) -> dict:
	url = "https://hotels4.p.rapidapi.com/locations/v2/search"
	querystring = {"query": city, "locale": "en_US", "currency": "RUB"}
	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": api_host
	}
	try:
		logger.info('Отправка запроса для получения отелей согласно расположению ')
		response = requests.request("GET", url, headers=headers, params=querystring)
		result = json.loads(response.text)
		list_destinations = {}

		for i in result["suggestions"]:
			if not isinstance(i, dict):
				continue
			for k in i['entities']:
				for caption in k["caption"].split(','):
					if caption.strip(' ') == city:
						if k["name"] not in list_destinations.keys():
							list_destinations[k["name"]] = k["destinationId"]
		return list_destinations
	except Exception:
		logger.info(f'result вернуло {result} ')
		print('Исключение')


#получение списка ид для получения подробной информации об отеле
def need_result(result, data):
	logger.info(f'Получение списка В need result data{data}')
	logger.info(f'тип списка В need result data{type(data)}')
	logger.info(f'Получение списка В need result data.keys{data.keys}')
	logger.info('Получение списка ИД для запроса более подробной информации')
	res = find_dict_key(result, 'results')
	logger.info(f'РЕЗУЛЬТАТЫ res {res}')
	list_results = []
	distances = []
	if 'distance' not in data:
		for k in res:
			list_results.append(k['id'])
			distances.append(k['landmarks'][0]['distance'].split(' ')[0])

		return list_results, distances

	for k in res:
		logger.info(f'вот data test_distance {data}')

		test_id, distance = test_distance(k, data)
		logger.info(f'test_id {test_id}')
		if test_id is not None:
			logger.info('вот id')
			logger.info(test_id)
			list_results.append(test_id)
			distances.append(distance)

	return list_results, distances


def test_distance(k, data):
	logger.info(f"РЕЗУЛЬТАТЫ k in res {k}")
	distance = float(k['landmarks'][0]['distance'].split(' ')[0])
	data_distance = float(data['distance'])
	logger.info(distance)
	logger.info(k['id'])
	logger.info(f'вот test_distance data distance{data["distance"]}')
	if distance <= data_distance:
		logger.info('вот ид')
		logger.info(k['id'])
		return k['id'], distance
	else:
		return None, None


#получение детализации предложений для бронирования
def get_details(id,check_in,check_out,distance):

	url = "https://hotels4.p.rapidapi.com/properties/get-details"
	querystring = {"id": id, "checkIn": check_in, "checkOut": check_out, "adults1": "1", "currency": "USD",
				   "locale": "en_US"}

	headers = {
		"X-RapidAPI-Key": api_key,
		"X-RapidAPI-Host": api_host
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	mes_to_tg =	post_to_tg(result, distance)
	return mes_to_tg


def post_to_tg(response, distance) -> str:
	logger.info('Обработка полученных данных о номере')
	suggestion = dict()
	text = ''
	suggestion['Название отеля'] = find_dict_key(response, 'name')
	suggestion['Рейтинг'] = find_dict_key(response, 'starRating')
	suggestion['Адрес'] = find_dict_key(response, 'addressLine1')
	suggestion['Расстояние от центра'] = distance
	suggestion['Cтоимость за ночь'] = find_dict_key(response, 'formatted')
	suggestion['Общая стоимость'] = find_dict_key(response, 'fullyBundledPricePerStay')
	if suggestion['Общая стоимость'] is not None:
		suggestion['Общая стоимость'] = suggestion['Общая стоимость'].split(' ')[1]
	else:
		suggestion['Общая стоимость'] = suggestion['Cтоимость за ночь']
	for key, val in suggestion.items():
		text += f"{str(key)}: {str(val)}\n"
	return text


#функция поиска по словарю
def find_dict_key(name_of_dict: dict, key: str) -> [str, dict]:

	if key in name_of_dict.keys():
		find = name_of_dict[key]
		return find
	for k in name_of_dict.keys():
		if isinstance(name_of_dict[k], dict):
			find = find_dict_key(name_of_dict[k], key)
			if find:
				return find


#получение списка отелей по расположению
def list_hotels_by_destination(message):

	with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
		logger.info('получение списка отелей по расположению')
		destination_id = data['city_id']
		check_in = data['check_in']
		check_out = data['check_out']
		sortorder = data['sortOrder']
		url = "https://hotels4.p.rapidapi.com/properties/list"
		querystring = {"destinationId": destination_id, "pageNumber": "1"
			, "pageSize": "4", "checkIn": check_in, "checkOut": check_out, "adults1": "1"
			, "sortOrder": sortorder
			, "locale": "en_US", "currency": "USD"}

		if 'start_price' in data.keys():
			querystring["priceMin"] = data['start_price']
			querystring["priceMax"] = data['end_price']

		headers = {
			"X-RapidAPI-Key": api_key,
			"X-RapidAPI-Host": api_host
		}
		response = requests.request("GET", url, headers=headers, params=querystring)
		result = json.loads(response.text)
		logger.info(f'list_hotels_by_destination data{data}')
		logger.info(f'list_hotels_by_destination data.keys{data.keys}')
		list_hotels, distance = need_result(result, data)
		logger.info('результаты перед return из list_hotels_by_destination')
		return list_hotels, distance
