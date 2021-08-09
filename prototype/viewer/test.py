import requests
from prototype import Config

url = f"http://{Config.RECEIVER_ADDRESS_TEST}:{Config.FILE_PORT}/connect"
r = requests.get(url)

url = f"http://{Config.RECEIVER_ADDRESS_TEST}:{Config.FILE_PORT}/{Config.FILE_EVENT}"
files = {'files': open('icon.png', 'rb')}
values = {'x': 100, 'y': 250}

r = requests.post(url, files=files, data=values)
