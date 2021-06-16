import threading
from evdev import InputDevice, ecodes, events
from streamer import Streamer
from accessor import Accessor
from server import Server
from client import Client
import Config

def start_host():
    server = Server()
    server.start()

def start_stream():
    streamer = Streamer()
    streamer.open_stream()
    streamer.start_stream()

def start_client():
    client = Client()
    client.connect()
    device = InputDevice('/dev/input/event11')
    print(device)
    client.listen_on_device(device)

def access_stream():
    accessor = Accessor()
    accessor.access_stream()


if Config.IS_HOST:
    threading.Thread(target=start_host).start()
    threading.Thread(target=start_stream).start()
else:
    threading.Thread(target=start_client).start()
    threading.Thread(target=access_stream).start()


