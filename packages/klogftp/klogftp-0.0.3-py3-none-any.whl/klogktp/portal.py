import requests


class Portal():
	
	def __init__(self, url, username, password) -> None:
		self.url = url
		self.username = username
		self.password = password

	def get_portal_token(self):
		portal_token = requests.get(f"{self.url}/aircast/default/login_take_token?username={self.username}&password={self.password}").json()['token']
		if portal_token: return portal_token
		else: return False

	def get_portal_user(self, **kwargs):
		data = []
		portal_token = self.get_portal_token()
		if 'staff_id' in kwargs:
			data = requests.get(f"{self.url}/aircast/default/display_auth_user?_token={portal_token}&staff_id={kwargs['staff_id']}").json()
		elif 'username' in kwargs:
			data = requests.get(f"{self.url}/aircast/default/display_auth_user?_token={portal_token}&username={kwargs['username']}").json() 
		else:
			data = requests.get(f"{self.url}/aircast/default/display_auth_user?_token={portal_token}").json()       
		if data: return data
		else: return False
	
	def display_resigned_staff(self):
		portal_token = self.get_portal_token()
		data = requests.get(f"{self.url}/aircast/default/display_resigned_staff?_token={portal_token}")
		return data.json()