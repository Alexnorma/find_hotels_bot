import json
import requests


def get_distination(city):
	url = "https://hotels4.p.rapidapi.com/locations/v2/search"

	querystring = {"query":"new york","locale":"en_US","currency":"USD"}

	headers = {
		"X-RapidAPI-Key": "8ad1568503msh9882a45583ee7a3p1a3cb6jsn2334ba5af675",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)

	for i in result["suggestions"]:
		if not isinstance(i, dict):
			continue
		if i['group'] != "CITY_GROUP":
			continue
		for k in i['entities']:
			if lower(k["name"] == city:
				return str(k['destinationId'])


def list_hotels_by_destination(city):
	url = "https://hotels4.p.rapidapi.com/properties/list"
	print('1')
	querystring = {"destinationId": get_distination(city), "pageNumber":"1","pageSize":"25","checkIn":"2022-08-04","checkOut":"2022-08-10","adults1":"1","sortOrder":"PRICE","locale":"en_US","currency":"USD"}

	headers = {
		"X-RapidAPI-Key": "8ad1568503msh9882a45583ee7a3p1a3cb6jsn2334ba5af675",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	print(result)




#
# with open('new.json','w') as file:
# 	json.dump(result, file, indent=4)