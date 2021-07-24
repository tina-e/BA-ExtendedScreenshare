from evdev import InputDevice

IS_STREAMER = False
STREAMER_ADDRESS = '192.168.178.23'
RECEIVER_ADDRESS = '192.168.178.136'

STREAM_PORT = 5000
EVENT_PORT = 8000

MOUSE_EVENT = 'mouseevent'
CAP_EVENT = 'capevent'

RESOLUTION_X = 1366
RESOLUTION_Y = 768
KEYBOARD_DEVICE_STREAMER = InputDevice('/dev/input/event4') #keyboard
MOUSE_DEVICE_STREAMER_POINT = InputDevice('/dev/input/event9') #mouse pointer (see xinput list: only listed at pointer)
MOUSE_DEVICE_STREAMER_CLICK = InputDevice('/dev/input/event6') #mouse keys (see xinput list: listed at pointer AND keyboard)

START_X = 10
START_Y = 10
END_X = 500
END_Y = 300
WIDTH = END_X - START_X
HEIGHT = END_Y - START_Y
BORDER_WIDTH = 2