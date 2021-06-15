import threading

from Streamer import Streamer
from Accessor import Accessor
import Config

start_x = 50
start_y = 50
end_x = 800
end_y = 750

def stream():
    streamer = Streamer(Config.RECEIVER, Config.PORT, start_x, start_y, end_x, end_y)
    streamer.open_stream()
    streamer.start_stream()

def access():
    accessor = Accessor()
    accessor.access_stream()

threading.Thread(target=stream).start()
threading.Thread(target=access).start()
