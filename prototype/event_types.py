from enum import IntEnum
from pynput.mouse import Button

class EventTypes(IntEnum):
    MOUSE_MOVEMENT = 0
    MOUSE_CLICK = 1
    MOUSE_SCROLL = 2
    KEYBOARD = 3
    CAPABILITY_MOUSE = 4
    CAPABILITY_KEYBOARD = 5

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