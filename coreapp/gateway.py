import requests
import asyncio
import httpx
from asgiref.sync import sync_to_async

def get_user_gdrive_status(user_id: int):
	url = "http://172.22.0.2/api/integ/gdrive/status/user/"
	response = requests.get(f'{url}{user_id}')
	response = response.json()
	return response['integrado']

def get_gdrive_integ_link(user_id: int):
	url = "http://172.22.0.2/api/integ/gdrive/oauth/user/"
	print(f'{url}{user_id}')
	response = requests.get(f'{url}{user_id}')
	response = response.text
	response = response[1:-1]
	return response

# @sync_to_async
async def update_gdrive_records(users: list):
	async with httpx.AsyncClient(timeout=None) as client:
	# client = httpx.Client(timeout=None)  # Disable all timeouts by default.
		response_dict = dict()
		# print(type(users))
		for user in users:
			url = f"http://pbla_gdrive_1/api/integ/gdrive/user/update/records?user_id={user}"
			response = await asyncio.gather(client.post(url))
			# print("           full response:", response.text)
			# print("           status_code:", response.status_code)
			# response_dict['user '+str(user)] = [response.status_code, response.text]
	# print(response_dict)
	return response


# def update_gdrive_records(user_id: int):
# 	url = f"http://pbla_gdrive_1/api/integ/gdrive/user/update/records?user_id={user_id}"
# 	response = requests.post(url)
# 	print(response)
# 	return response.status_code