from evdev import InputDevice
import pyautogui
import socket

# IPs and Ports
DEVICE_ADDRESS_LIST = [('tina-EasyNote-TH36', '192.168.178.23'), ('tinapc', '192.168.178.136')]
STREAMER_ADDRESS = ''
RECEIVER_ADDRESS = ''
IS_STREAMER = False

STREAMER_ADDRESS_TEST = '192.168.178.23'
RECEIVER_ADDRESS_TEST = '192.168.178.136'

def set_ips():
    global STREAMER_ADDRESS, RECEIVER_ADDRESS, IS_STREAMER
    if IS_STREAMER:
        if DEVICE_ADDRESS_LIST[0][0] == socket.gethostname():
            STREAMER_ADDRESS = DEVICE_ADDRESS_LIST[0][1]
            RECEIVER_ADDRESS = DEVICE_ADDRESS_LIST[1][1]
        else:
            STREAMER_ADDRESS = DEVICE_ADDRESS_LIST[1][1]
            RECEIVER_ADDRESS = DEVICE_ADDRESS_LIST[0][1]
    else:
        if DEVICE_ADDRESS_LIST[0][0] == socket.gethostname():
            STREAMER_ADDRESS = DEVICE_ADDRESS_LIST[1][1]
            RECEIVER_ADDRESS = DEVICE_ADDRESS_LIST[0][1]
        else:
            STREAMER_ADDRESS = DEVICE_ADDRESS_LIST[0][1]
            RECEIVER_ADDRESS = DEVICE_ADDRESS_LIST[1][1]
    print("REC:", RECEIVER_ADDRESS)
    print("STR:", STREAMER_ADDRESS)

def get_str_addr():
    global STREAMER_ADDRESS
    return STREAMER_ADDRESS

def get_rec_addr():
    global RECEIVER_ADDRESS
    return RECEIVER_ADDRESS


STREAM_PORT = 5000
EVENT_PORT = 8000
FILE_PORT = 9999
FILE_EVENT = 'fileevent'

# GUI
RESOLUTION_X = pyautogui.size().width
RESOLUTION_Y = pyautogui.size().height

START_X = 0
START_Y = 0
END_X = RESOLUTION_X
END_Y = RESOLUTION_Y
WIDTH = END_X - START_X
HEIGHT = END_Y - START_Y

def set_coords(dimensions):
    global START_X, START_Y, END_X, END_Y, WIDTH, HEIGHT
    START_X = dimensions[0]
    START_Y = dimensions[1]
    END_X = dimensions[2]
    END_Y = dimensions[3]
    WIDTH = END_X - START_X
    HEIGHT = END_Y - START_Y

def get_coords():
    global START_X, START_Y, END_X, END_Y, WIDTH, HEIGHT
    return START_X, START_Y, WIDTH, HEIGHT


BORDER_WIDTH = 2

STREAM_ACTIVE = False

def toggle_stream_activity():
    global STREAM_ACTIVE
    STREAM_ACTIVE = not STREAM_ACTIVE

# Input Devices
KEYBOARD_DEVICE_STREAMER = InputDevice('/dev/input/event4') #keyboard
MOUSE_DEVICE_STREAMER_POINT = InputDevice('/dev/input/event9') #mouse pointer (see xinput list: only listed at pointer)
MOUSE_DEVICE_STREAMER_CLICK = InputDevice('/dev/input/event6') #mouse keys (see xinput list: listed at pointer AND keyboard)


#MOUSE_EVENT = 'mouseevent'
#CAP_EVENT = 'capevent'

