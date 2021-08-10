import time

import json
import http.client as client

import requests

#from prototype import Config


class FileClient:
    def __init__(self, configurator):
        self.config = configurator
        print("addr", self.config.STREAMER_ADDRESS)
        self.connection = client.HTTPConnection(self.config.STREAMER_ADDRESS_TEST, self.config.FILE_PORT)

    def connect(self):
        self.connection.connect()
        self.connection.request('GET', f"http://{self.config.STREAMER_ADDRESS_TEST}:{self.config.FILE_PORT}/connect")
        response = self.connection.getresponse()
        print(response)

    def send_file(self, filename, mimetype, drop_x, drop_y):
        url = f"http://{self.config.STREAMER_ADDRESS_TEST}:{self.config.FILE_PORT}/{self.config.FILE_EVENT}"
        filename = filename.replace('\r', '')
        filename = filename.replace('\n', '')
        files = {"files": open(filename, 'rb')}
        data = {"filename": filename.split('/')[-1], "mimetype": mimetype, "x": drop_x, "y": drop_y}
        r = requests.post(url, files=files, data=data)
        print(r.status_code)

    # def receive_file(self):
    #    data = request.json

#client = Client()
#client.connect()
#client.send_file("icon.png", 100, 100)
