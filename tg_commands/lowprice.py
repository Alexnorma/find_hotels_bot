import json
import requests


#получение конкретного места для поиска номеров
def get_distination(city: str) -> dict:
	url = "https://hotels4.p.rapidapi.com/locations/v2/search"
	querystring = {"query": city, "locale": "en_US", "currency": "RUB"}
	headers = {
		"X-RapidAPI-Key": "9a7ccb7d9amsh1a4d3094da8696ep1a185ejsn051d4a950b17",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
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
	with open('details.json', 'w') as file:
		json.dump(result, file, indent=4)
	mes_to_tg =	post_to_tg(result)
	return mes_to_tg


def post_to_tg(response) -> str:
	suggestion = dict()
	text = ''
	suggestion['Название отеля'] = find_dict_key(response, 'name')
	suggestion['Рейтинг'] = find_dict_key(response, 'starRating')
	suggestion['Адрес'] = find_dict_key(response, 'addressLine1')
	suggestion['Cтоимость за ночь'] = find_dict_key(response, 'current')
	suggestion['Общая стоимость'] = find_dict_key(response, 'fullyBundledPricePerStay').split(' ')[1]
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
	with open('results.json', 'w') as file:
		json.dump(a, file, indent=4)
	return a





#
# with open('new.json','w') as file:
# 	json.dump(list_hotels_by_destination('New York'), file, indent=4)