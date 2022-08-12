import json
import requests



def get_distination(city):
	url = "https://hotels4.p.rapidapi.com/locations/v2/search"

	querystring = {"query": city, "locale": "en_US", "currency": "USD"}

	headers = {
		"X-RapidAPI-Key": "8ad1568503msh9882a45583ee7a3p1a3cb6jsn2334ba5af675",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)
	# list_destinations = {}
	# for i in result["suggestions"]:
	# 	if not isinstance(i, dict):
	# 		continue
	# 	for k in i['entities']:
	# 		for caption in k["caption"].split(','):
	# 			if caption.strip(' ') == city:
	# 				if k["name"] not in list_destinations.keys():
	# 					list_destinations[k["name"]] = k["destinationId"]
	return result
print(get_distination('New York'))

def need_result(result):

	data = result["data"]
	body = data["body"]
	search = body['searchResults']
	res = search['results']
	list_results = []
	for count in range(1):
		list_results.append(res[count])
	return list_results


def list_hotels_by_destination(city):
	url = "https://hotels4.p.rapidapi.com/properties/list"
	querystring = {"destinationId": get_distination(city), "pageNumber":"1"
		,"pageSize": "25", "checkIn":'2022-08-10', "checkOut": '2022-08-15', "adults1": "1", "sortOrder": "PRICE"
		, "locale":"en_US", "currency": "USD"}

	headers = {
		"X-RapidAPI-Key": "8ad1568503msh9882a45583ee7a3p1a3cb6jsn2334ba5af675",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	result = json.loads(response.text)

	a = need_result(result)

	return a

#
# def get_check_in_date(date):
# 	check_in = str(date)
# 	return check_in
#
#
# def get_check_out_date(date):
# 	check_out = str(date)
# 	return check_out






#
# with open('new.json','w') as file:
# 	json.dump(list_hotels_by_destination('New York'), file, indent=4)