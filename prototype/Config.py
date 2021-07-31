from evdev import InputDevice
import pyautogui
import socket

# IPs and Ports
DEVICE_ADDRESS_LIST = [('tina', '192.168.178.23'), ('tinapc', '192.168.178.136')]
STREAMER_ADDRESS = ''
RECEIVER_ADDRESS = ''
IS_STREAMER = False


def set_ips():
    global STREAMER_ADDRESS, RECEIVER_ADDRESS
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


STREAM_PORT = 5000
EVENT_PORT = 8000

# GUI
RESOLUTION_X = pyautogui.size().width
RESOLUTION_Y = pyautogui.size().height

START_X = 0
START_Y = 0
END_X = 0
END_Y = 0

def set_coords(dimensions):
    global START_X, START_Y, END_X, END_Y
    START_X = dimensions[0]
    START_Y = dimensions[1]
    END_X = dimensions[2]
    END_Y = dimensions[3]

WIDTH = END_X - START_X
HEIGHT = END_Y - START_Y

BORDER_WIDTH = 2

# Input Devices
KEYBOARD_DEVICE_STREAMER = InputDevice('/dev/input/event4') #keyboard
MOUSE_DEVICE_STREAMER_POINT = InputDevice('/dev/input/event9') #mouse pointer (see xinput list: only listed at pointer)
MOUSE_DEVICE_STREAMER_CLICK = InputDevice('/dev/input/event6') #mouse keys (see xinput list: listed at pointer AND keyboard)


#MOUSE_EVENT = 'mouseevent'
#CAP_EVENT = 'capevent'
