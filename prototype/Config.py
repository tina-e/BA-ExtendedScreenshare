from evdev import InputDevice

IS_STREAMER = True
STREAMER_ADDRESS = '192.168.178.136'
RECEIVER_ADDRESS = '192.168.178.23'

STREAM_PORT = 5000
EVENT_PORT = 8000

MOUSE_EVENT = 'mouseevent'
CAP_EVENT = 'capevent'

KEYBOARD_DEVICE_STREAMER = InputDevice('/dev/input/event4')
MOUSE_DEVICE_STREAMER_POINT = InputDevice('/dev/input/event9')
MOUSE_DEVICE_STREAMER_CLICK = InputDevice('/dev/input/event6')

START_X = 10
START_Y = 200
END_X = 600
END_Y = 735