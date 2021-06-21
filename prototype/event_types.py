from enum import Enum

class EventTypes(Enum):
    MOUSE_MOVEMENT = 0
    MOUSE_CLICK = 1
    MOUSE_SCROLL = 2
    KEYBOARD = 3
    CAPABILITY_MOUSE = 4
    CAPABILITY_KEYBOARD = 5