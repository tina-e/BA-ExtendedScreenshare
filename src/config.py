import pyautogui
import socket
import pathlib


class Configurator:
    def __init__(self, args):
        self.STREAM_ACTIVE = False
        self.IS_STREAMER = False
        self.PROJECT_PATH_ABSOLUTE = pathlib.Path(__file__).parent.resolve()
        # IPs and Ports
        self.OWN_IP = self.get_own_ip()
        self.ODD_IP = self.get_own_ip()
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
        self.KEYBOARD_DEVICE_PATH = args[1]
        self.MOUSE_DEVICE_PATH = args[2]

    def get_own_ip(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('10.255.255.255', 1))
        ip = sock.getsockname()[0]
        sock.close()
        return ip

    def set_streamer_ip(self, ip):
        if ip is None:
            self.STREAMER_ADDRESS = self.OWN_IP
        else:
            self.STREAMER_ADDRESS = ip
            self.ODD_IP = ip

    def set_receiver_ip(self, ip):
        if ip is None:
            self.RECEIVER_ADDRESS = self.OWN_IP
        else:
            self.RECEIVER_ADDRESS = ip
            self.ODD_IP = ip

    def write_clipboard_config(self):
        with open(f"{self.PROJECT_PATH_ABSOLUTE}/clipboard/clipboard_bridge/config/config.ini", "a") as file:
            file.write(f"\nmain_server_address = http://{self.ODD_IP}:5000/")
            file.write(f"\ndomain = http://{self.OWN_IP}")
            file.close()

    def clean_clipboard_config(self):
        print("CLEAN")
        with open(f"{self.PROJECT_PATH_ABSOLUTE}/clipboard/clipboard_bridge/config/config.ini", "w") as file:
            file.write("[networking]\n")
            file.write("port = 5010\n")
            file.write("is_syncing = True")
            file.close()

    def set_coords(self, dimensions):
        self.START_X = dimensions[0]
        self.START_Y = dimensions[1]
        self.END_X = dimensions[2]
        self.END_Y = dimensions[3]
        self.WIDTH = self.END_X - self.START_X
        self.HEIGHT = self.END_Y - self.START_Y

    def toggle_stream_activity(self):
        self.STREAM_ACTIVE = not self.STREAM_ACTIVE
