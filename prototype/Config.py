from evdev import InputDevice

IS_STREAMER = False
STREAMER_ADDRESS = '192.168.178.169'
RECEIVER_ADDRESS = '192.168.178.136'

STREAM_PORT = 5000
EVENT_PORT = 8000

CAP_PORT = 8000
MOUSE_EVENT = 'mouseevent'
CAP_EVENT = 'capevent'

KEYBOARD_DEVICE_STREAMER = InputDevice('/dev/input/event0')
MOUSE_DEVICE_STREAMER_POINT = InputDevice('/dev/input/event1')
MOUSE_DEVICE_STREAMER_CLICK = InputDevice('/dev/input/event2')

START_X = 50
START_Y = 50
END_X = 800
END_Y = 750