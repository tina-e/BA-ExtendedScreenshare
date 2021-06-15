from Streamer import Streamer
from Accessor import Accessor
import Config

start_x = 50
start_y = 50
end_x = 800
end_y = 750

streamer = Streamer(Config.HOST, Config.PORT, start_x, start_y, end_x, end_y)
accessor = Accessor()

streamer.open_stream()
streamer.start_stream()

accessor.access_stream()