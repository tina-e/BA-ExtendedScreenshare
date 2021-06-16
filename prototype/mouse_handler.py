import json

from evdev import UInput, ecodes
import Config

# specify capabilities for our virtual input device
cap_mouse = {
    ecodes.EV_REL: (ecodes.REL_X, ecodes.REL_Y),
    ecodes.EV_KEY: (ecodes.BTN_LEFT, ecodes.BTN_RIGHT),
}
mouse_ui = UInput(cap_mouse, name="mouse")

def add_cursor():
    mouse_ui.write(ecodes.EV_REL, ecodes.REL_X, Config.START_X)
    mouse_ui.write(ecodes.EV_REL, ecodes.REL_Y, Config.START_Y)
    mouse_ui.syn()
    #with UInput(cap_mouse, name="mouse") as mouse_ui:
    #    mouse_ui.write(ecodes.EV_REL, ecodes.REL_X, Config.START_X)
    #    mouse_ui.write(ecodes.EV_REL, ecodes.REL_Y, Config.START_Y)
    #    mouse_ui.syn()

def map_input(data):
    print("test")
    event_dict = json.loads(data)
    mouse_ui.write(event_dict["type"], event_dict["code"], event_dict["val"])
    mouse_ui.syn()