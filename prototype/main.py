import threading
from evdev import InputDevice, ecodes, events
from streamer import Streamer
from accessor import Accessor
from server import Server
from event_receiver import Receiver
from event_sender import Sender
from client import Client
import Config


def start_stream():
    streamer = Streamer()
    streamer.open_stream()
    streamer.start_stream()

def access_stream():
    accessor = Accessor()
    accessor.access_stream()


#def start_host():
    # server = Server()
    # server.start()

#def start_client():
    # client = Client()
    # client.connect()
    # client.listen_on_device()
    # client.listen_on_device_abs()


def start_event_receiver():
    rec = Receiver()

def start_event_sender():
    sen = Sender()




if Config.IS_STREAMER:
    #threading.Thread(target=start_host).start()
    threading.Thread(target=start_event_receiver())
    threading.Thread(target=start_stream).start()
else:
    access_stream()
    print("stream running")
    #start_client()
    start_event_sender()
    #threading.Thread(target=start_client).start()
    #threading.Thread(target=access_stream).start()


