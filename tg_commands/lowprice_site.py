import json
import requests
import re
#получение фото
def get_photos(id: str):
	url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
	querystring = {"id": id}

	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	return result
#обработка фоток
def process_photos(id: str, count_photos: str) -> list:
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


#
#
#получение списка ид для получения подробной информации об отеле
def need_result(result)->list:

	data = result["data"]
	body = data["body"]
	search = body['searchResults']
	res = search['results']
	list_results = []
	for k in res:
		list_results.append(k['id'])
	return list_results
#
#
#получение детализации предложений для бронирования
def get_details(id):
	url = "https://hotels4.p.rapidapi.com/properties/get-details"
	querystring = {"id": id, "checkIn": '2022-09-01', "checkOut": '2022-09-03', "adults1": "1", "currency": "USD",
				   "locale": "en_US"}

	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	mes_to_tg =	post_to_tg(result)
	return mes_to_tg
#
#
def post_to_tg(response) -> str:
	suggestion = dict()
	text = ''
	suggestion['Название отеля'] = find_dict_key(response, 'name')
	suggestion['Рейтинг'] = find_dict_key(response, 'starRating')
	suggestion['Адрес'] = find_dict_key(response, 'addressLine1')
	suggestion['Cтоимость за ночь'] = find_dict_key(response, 'formatted')

	suggestion['Общая стоимость'] = find_dict_key(response, 'fullyBundledPricePerStay')
	if suggestion['Общая стоимость'] is not None:
		suggestion['Общая стоимость'] = suggestion['Общая стоимость'].split(' ')[1]
	else:
		suggestion['Общая стоимость'] = suggestion['Cтоимость за ночь']
	for key, val in suggestion.items():
		text += f"{str(key)}: {str(val)}\n"
	return text


def find_dict_key(name_of_dict: dict, key: str) -> [str, dict]:

	if key in name_of_dict.keys():
		find = name_of_dict[key]
		return find
	for k in name_of_dict.keys():
		if isinstance(name_of_dict[k], dict):
			find = find_dict_key(name_of_dict[k], key)
			if find:
				return find



def list_hotels_by_destination(data_query: dict):
	destination_id = data_query['id']
	check_in = data_query['check_in']
	check_out = data_query['check_out']
	url = "https://hotels4.p.rapidapi.com/properties/list"
	querystring = {"destinationId": destination_id, "pageNumber":"1"
		,"pageSize": "2", "checkIn":check_in, "checkOut": check_out, "adults1": "1", "sortOrder": "PRICE"
		, "locale":"en_US", "currency": "USD"}
	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)

	a = need_result(result)

	return a
