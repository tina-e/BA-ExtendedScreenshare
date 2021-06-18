import json

from evdev import UInput, ecodes
import Config

mouse_ui = None
key_ui = None

def add_cursor(mouse_capas, key_capas):
    # specify capabilities for our virtual input device
    #cap_mouse = {
    #    ecodes.EV_REL: (ecodes.REL_X, ecodes.REL_Y),
    #    ecodes.EV_KEY: (ecodes.BTN_LEFT, ecodes.BTN_RIGHT),
    #}

    mouse_ui = UInput(mouse_capas, name="mouse")
    key_ui = UInput(key_capas, name="key")

    mouse_ui.write(ecodes.EV_REL, ecodes.REL_X, Config.START_X)
    mouse_ui.write(ecodes.EV_REL, ecodes.REL_Y, Config.START_Y)
    mouse_ui.syn()
    #with UInput(cap_mouse, name="mouse") as mouse_ui:
    #    mouse_ui.write(ecodes.EV_REL, ecodes.REL_X, Config.START_X)
    #    mouse_ui.write(ecodes.EV_REL, ecodes.REL_Y, Config.START_Y)
    #    mouse_ui.syn()

def map_input(data):
    mouse_ui.write(data["type"], data["code"], data["val"])
    mouse_ui.syn()