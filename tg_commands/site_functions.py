import json
import requests
import re
from loguru import logger


#получение фото
@logger.catch()
def get_photos(id: str) -> dict:

	url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
	querystring = {"id": id}
	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	logger.info('Отправка запроса для получения фото')
	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	return result


#обработка фоток
def process_photos(id: str, count_photos: str) -> list:
	logger.info('Обработка фото')
	all_photo = get_photos(id)
	data_photos = all_photo['hotelImages']
	pattern = r'{size}'
	list_photos = [data_photos[i]['baseUrl'] for i in range(0, int(count_photos))]
	resize_photos = [re.sub(pattern, 'z', item) for item in list_photos]
	return resize_photos


#получение конкретного места для поиска номеров
def get_distination(city: str) -> dict:
	url = "https://hotels4.p.rapidapi.com/locations/v2/search"
	querystring = {"query": city, "locale": "en_US", "currency": "RUB"}
	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
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
	except BaseException:
		print('Исключение')


#получение списка ид для получения подробной информации об отеле
def need_result(result, data_query) -> tuple:
	logger.info('Получение списка ИД для запроса более подробной информации')
	res = find_dict_key(result, 'results')
	print(res)
	list_results = []
	if 'distance' not in data_query.keys():
		for k in res:
			list_results.append(k['id'])
	for k in res:
		test_id, distance = test_distance(k, data_query)
		list_results.append(test_id)
	return list_results, distance


def test_distance(k, data_query):
	distance = k['landmarks'][0]['distance']
	if distance <= data_query['distance']:
		return k['id'], distance


#получение детализации предложений для бронирования
def get_details(id,check_in,check_out,distance):
	logger.info(f'Получение информации о номере c ИД {id}')
	url = "https://hotels4.p.rapidapi.com/properties/get-details"
	querystring = {"id": id, "checkIn": check_in, "checkOut": check_out, "adults1": "1", "currency": "USD",
				   "locale": "en_US"}

	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
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
def list_hotels_by_destination(data_query: dict):
	logger.info('получение списка отелей по расположению')
	destination_id = data_query['id']
	check_in = data_query['check_in']
	check_out = data_query['check_out']
	url = "https://hotels4.p.rapidapi.com/properties/list"
	querystring = {"destinationId": destination_id, "pageNumber": "1"
		, "pageSize": "4", "checkIn": check_in, "checkOut": check_out, "adults1": "1"
		, "sortOrder": data_query['sortOrder']
		, "locale": "en_US", "currency": "USD"}
	if 'start_price' in data_query.keys():
		querystring["priceMin"] = data_query['start_price']
		querystring["priceMax"] = data_query['end_price']

	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	list_hotels, distance = need_result(result, data_query)

	return list_hotels, distance
