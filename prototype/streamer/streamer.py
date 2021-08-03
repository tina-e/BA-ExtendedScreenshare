from threading import Thread
import time

# https://www.youtube.com/watch?v=HDY8pf-b1nA
# sudo apt install python3-gst-1.0


import Config



from streamer.stream import Stream
from streamer.mouse_handler import EventHandlerEvdev

#from streamer.mouse_handler_autogui import EventHandler
from event_types import EventTypes, get_button_by_id
import socket
import threading

class Streamer:
    def __init__(self):
        # stream
        self.stream = Stream()
        self.is_stream_running = False
        # event communication
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((Config.STREAMER_ADDRESS, Config.EVENT_PORT))
        self.event_handler = EventHandlerEvdev()
        #self.event_handler = EventHandler()
        connection_thread = threading.Thread(target=self.receive, daemon=True)
        connection_thread.start()

    def send_stream_coords(self):
        #time.sleep(10)
        print("sending coords")
        message = EventTypes.STREAM_COORDS.to_bytes(1, 'big')
        message += Config.START_X.to_bytes(2, 'big')
        message += Config.START_Y.to_bytes(2, 'big')
        message += Config.END_X.to_bytes(2, 'big')
        message += Config.END_Y.to_bytes(2, 'big')
        self.sock.sendto(message, (Config.RECEIVER_ADDRESS, Config.EVENT_PORT))

    def receive(self):
        print("Waiting for viewer...")
        receiving = True
        while receiving:
            data, addr = self.sock.recvfrom(1024)
            try:
                event_type = EventTypes(data[0])
                if event_type == EventTypes.REGISTER:
                    self.send_stream_coords()
                elif event_type == EventTypes.VIEWING:
                    is_viewing = data[1]
                    print(f"is someone watching stream? {is_viewing}")
                    self.handle_view(is_viewing)
                elif self.is_stream_running:
                    if event_type == EventTypes.MOUSE_MOVEMENT:
                        event_x = int.from_bytes(data[1:3], 'big')
                        event_y = int.from_bytes(data[3:5], 'big')
                        # print(f"moved {event_x}, {event_y}")
                        self.event_handler.map_mouse_movement(event_x, event_y)
                    elif event_type == EventTypes.MOUSE_CLICK:
                        event_x = int.from_bytes(data[1:3], 'big')
                        event_y = int.from_bytes(data[3:5], 'big')
                        event_button = get_button_by_id(data[5])
                        event_was_pressed = data[6]
                        #print(f"clicked at {event_x}, {event_y} with button {event_button}; pressed: {event_was_pressed}")
                        self.event_handler.map_mouse_click(event_x, event_y, event_button, event_was_pressed)
                    elif event_type == EventTypes.MOUSE_SCROLL:
                        event_dx = int.from_bytes(data[5:7], 'big', signed=True)
                        event_dy = int.from_bytes(data[7:9], 'big', signed=True)
                        #print(f"scrolled {event_dx}, {event_dy}")
                        self.event_handler.map_mouse_scroll(event_dx, event_dy)
                    elif event_type == EventTypes.KEYBOARD:
                        event_key = int.from_bytes(data[1:3], 'big')
                        event_value = data[3]
                        #print(f"key {event_key}: {event_value} (down=1, up=0, hold=2)")
                        self.event_handler.map_keyboard(event_key, event_value)
            except UnicodeDecodeError:
                continue

    def handle_view(self, is_viewing):
        if is_viewing:
            self.is_stream_running = True
            self.stream.start()
            self.event_handler.create_device()
            #self.send_stream_coords()
        elif self.is_stream_running:
            self.is_stream_running = False
            self.stream.end()
            self.event_handler.remove_device()
        else:
            self.stream.close()
            self.event_handler.remove_device()

    def close_stream(self):
        if self.is_stream_running:
            self.is_stream_running = False
            #self.stream.end()
            self.stream.close()
            self.event_handler.remove_device()
        else:
            self.stream.close()
            #self.event_handler.remove_device()


    #def pause_stream(self):
    #    self.pipeline.set_state(Gst.State.PAUSED)


##############################################################################################################################

# ! video/x-raw,width=750,height=500   legt größe des streams fest
# use-damage=0 angeblich CPU fordernd
# ximageslink creates window for output (glimagesink also possible, higher CPU required)
# ! videoscale method=0, auch wieder CPU sache scheinbar
# pipeline = Gst.parse_launch("ximagesrc startx=100 starty=10 endx=800 endy=800 ! video/x-raw,framerate=30/1 ! ximagesink")

# pipeline = Gst.parse_launch("rtpmp4vpay ! decodebin ! videoconvert ! autovideosink")
# pipeline = Gst.parse_launch("v4l2src ! decodebin ! videoconvert ! appsink name=sink")
# appsink = pipeline.get_by_name("sink")
# pipeline.set_state(Gst.State.PLAYING)
