from evdev import InputDevice
import pyautogui
import socket
import pathlib


class Configurator:
    def __init__(self):
        self.STREAM_ACTIVE = False
        self.IS_STREAMER = False
        # IPs and Ports
        self.DEVICE_ADDRESS_DICT = {'tina-EasyNote-TH36': '192.168.178.23', 'tinapc': '192.168.178.136'}
        self.STREAMER_ADDRESS = ''
        self.RECEIVER_ADDRESS = ''
        self.STREAM_PORT = 9000
        self.EVENT_PORT = 9900
        self.FILE_PORT = 9990
        self.FILE_EVENT = 'fileevent'

        # GUI
        self.RESOLUTION_X = pyautogui.size().width
        self.RESOLUTION_Y = pyautogui.size().height
        self.START_X = 0
        self.START_Y = 0
        self.END_X = self.RESOLUTION_X
        self.END_Y = self.RESOLUTION_Y
        self.WIDTH = self.END_X - self.START_X
        self.HEIGHT = self.END_Y - self.START_Y
        self.BORDER_WIDTH = 2

        # Input Devices
        self.KEYBOARD_DEVICE_STREAMER = InputDevice('/dev/input/event4')  # keyboard
        self.MOUSE_DEVICE_STREAMER_POINT = InputDevice('/dev/input/event9')  # mouse pointer (see xinput list: only listed at pointer)
        self.MOUSE_DEVICE_STREAMER_CLICK = InputDevice('/dev/input/event6')  # mouse keys (see xinput list: listed at pointer AND keyboard)

        # Path
        self.PROJECT_PATH_ABSOLUTE = pathlib.Path(__file__).parent.resolve()

    def set_streamer_ip(self, ip):
        if ip is None:
            self.STREAMER_ADDRESS = self.DEVICE_ADDRESS_DICT.get(socket.gethostname())
        else:
            self.STREAMER_ADDRESS = ip

    def set_receiver_ip(self, ip):
        if ip is None:
            self.RECEIVER_ADDRESS = self.DEVICE_ADDRESS_DICT.get(socket.gethostname())
        else:
            self.RECEIVER_ADDRESS = ip

    def set_coords(self, dimensions):
        self.START_X = dimensions[0]
        self.START_Y = dimensions[1]
        self.END_X = dimensions[2]
        self.END_Y = dimensions[3]
        self.WIDTH = self.END_X - self.START_X
        self.HEIGHT = self.END_Y - self.START_Y

    def toggle_stream_activity(self):
        self.STREAM_ACTIVE = not self.STREAM_ACTIVE
