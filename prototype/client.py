from evdev import InputDevice, ecodes as e, events
import Config
import json
import http.client as client

connection = client.HTTPConnection(Config.HOST, Config.PORT)
connection.connect()

device = InputDevice('/dev/input/event11')
print(device)

for event in device.read_loop():
    timestamp = event.timestamp()
    code = event.code
    type = event.type
    val = event.value
    _data = json.dumps({"event": str(event), "timestamp": timestamp, "code": code, "type": type, "val": val})
    headers = {'Content-type': 'application/json'}
    connection.request('POST', f'http://{Config.HOST}:{Config.PORT}/{Config.MOUSE_EVENT}', _data, headers)
    response = connection.getresponse()
