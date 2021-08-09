import time

import json
import http.client as client

import requests

from prototype import Config


class FileClient:
    def __init__(self):
        self.connection = client.HTTPConnection(Config.RECEIVER_ADDRESS_TEST, Config.FILE_PORT)

    def connect(self):
        self.connection.connect()
        self.connection.request('GET', f"http://{Config.RECEIVER_ADDRESS_TEST}:{Config.FILE_PORT}/connect")
        response = self.connection.getresponse()
        print(response)

    def send_file(self, filename, mimetype, drop_x, drop_y):
        url = f"http://{Config.RECEIVER_ADDRESS_TEST}:{Config.FILE_PORT}/{Config.FILE_EVENT}"
        files = {"files": open(filename, 'rb')}
        data = {"filename": filename, "mimetype": mimetype, "x": drop_x, "y": drop_y}
        r = requests.post(url, files=files, data=data)
        print(r.status_code)

    # def receive_file(self):
    #    data = request.json

#client = Client()
#client.connect()
#client.send_file("icon.png", 100, 100)
