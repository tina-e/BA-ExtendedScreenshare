import socket
import threading
import Config
from event_types import EventTypes, get_button_by_id


class Receiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((Config.STREAMER_ADDRESS, Config.EVENT_PORT))
        connection_thread = threading.Thread(target=self._receive)
        connection_thread.start()

    def _receive(self):
        _receiving = True
        while _receiving:
            data, addr = self.sock.recvfrom(1024)
            try:
                print("event received:")
                event_type = EventTypes(data[0])
                event_x = int.from_bytes(data[1:3], 'big')
                event_y = int.from_bytes(data[4:6], 'big')
                if event_type == EventTypes.MOUSE_MOVEMENT:
                    print(f"moved {event_x}, {event_y}")
                elif event_type == EventTypes.MOUSE_CLICK:
                    event_button = get_button_by_id(data[7])
                    event_was_pressed = data[8]
                    print(f"clicked at {event_x}, {event_y} with button {event_button}; pressed: {event_was_pressed}")
                elif event_type == EventTypes.MOUSE_SCROLL:
                    event_dx = int.from_bytes(data[7:9], 'big')
                    event_dy = int.from_bytes(data[10:12], 'big')
                    print(f"scrolled {event_dx}, {event_dy}")
                #TODO: verarbeite event
            except UnicodeDecodeError:
                continue
