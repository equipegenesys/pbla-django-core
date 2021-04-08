import requests

def get_user_gdrive_status(user_id: int):
	url = "http://172.22.0.2/api/integ/gdrive/status/user/"
	response = requests.get(f'{url}{user_id}')
	response = response.json()
	return response['integrado']

def get_gdrive_integ_link(user_id: int):
	url = "http://172.22.0.2/api/integ/gdrive/oauth/user/"
	response = requests.get(f'{url}{user_id}')
	response = response.text
	response = response[1:-1]
	return response