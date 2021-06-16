import Config
import json
import http.client as client

class Client:
    def __init__(self):
        self.connection = client.HTTPConnection(Config.HOST, Config.EVENT_PORT)

    def connect(self):
        self.connection.connect()

    def listen_on_device(self, device):
        for event in device.read_loop():
            print(event)
            timestamp = event.timestamp()
            code = event.code
            type = event.type
            val = event.value
            _data = json.dumps({"event": str(event), "timestamp": timestamp, "code": code, "type": type, "val": val})
            headers = {'Content-type': 'application/json'}
            self.connection.request('POST', f"http://{Config.HOST}:{Config.EVENT_PORT}/{Config.MOUSE_EVENT}", _data, headers)
            response = self.connection.getresponse()
