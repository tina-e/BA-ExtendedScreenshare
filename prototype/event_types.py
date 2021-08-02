from enum import IntEnum
from pynput.mouse import Button
from evdev import ecodes

class EventTypes(IntEnum):
    VIEWING = 0
    STREAM_COORDS = 1
    MOUSE_MOVEMENT = 2
    MOUSE_CLICK = 3
    MOUSE_SCROLL = 4
    KEYBOARD = 5
    PASTE = 6
    COPY = 7
    CAPABILITY_MOUSE = 8
    CAPABILITY_KEYBOARD = 9

def get_button_by_id(id):
    if id == 0: return Button.left
    elif id == 1: return Button.right
    elif id == 2: return Button.middle
    return None

def get_id_by_button(button):
    if button == Button.left: return 0
    elif button == Button.right: return 1
    elif button == Button.middle: return 2
    return None

def get_device_by_button(button):
    if button == Button.left: return ecodes.BTN_LEFT
    elif button == Button.right: return ecodes.BTN_RIGHT
    elif button == Button.middle: return ecodes.BTN_MIDDLE
    return None