import json

from evdev import UInput, ecodes
import Config

cap_mouse = {
    ecodes.EV_REL: (ecodes.REL_X, ecodes.REL_Y),
    ecodes.EV_KEY: (ecodes.BTN_LEFT, ecodes.BTN_RIGHT),
}
mouse_ui = UInput(cap_mouse, name="mouse")
# key_ui = UInput(key_capas, name="key")
mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, Config.START_X)
mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, Config.START_Y)
mouse_ui.syn()

def add_cursor(pos, mouse_capas, key_capas):
    # specify capabilities for our virtual input device
    cap_mouse = {
        ecodes.EV_REL: (ecodes.REL_X, ecodes.REL_Y),
        ecodes.EV_KEY: (ecodes.BTN_LEFT, ecodes.BTN_RIGHT),
    }

    print(cap_mouse)
    print(mouse_capas)

    mouse_ui = UInput(cap_mouse, name="mouse")
    #key_ui = UInput(key_capas, name="key")

    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, int(pos(0)))
    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, int(pos(0)))
    mouse_ui.syn()
    #with UInput(cap_mouse, name="mouse") as mouse_ui:
    #    mouse_ui.write(ecodes.EV_REL, ecodes.REL_X, Config.START_X)
    #    mouse_ui.write(ecodes.EV_REL, ecodes.REL_Y, Config.START_Y)
    #    mouse_ui.syn()

def map_input(data):
    mouse_ui.write(data["type"], data["code"], data["val"])
    mouse_ui.syn()