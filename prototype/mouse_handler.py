import json
import subprocess
import time

from evdev import UInput, ecodes
import Config

class InputDevice:
    def __init__(self):
        self.cap_mouse = {
            ecodes.EV_REL: (ecodes.REL_X, ecodes.REL_Y),
            ecodes.EV_KEY: (ecodes.BTN_LEFT, ecodes.BTN_RIGHT),
        }
        self.mouse_ui = UInput(self.cap_mouse, name='mouse')
        # self.key_ui = UInput(self.cap_key, name="key")

        subprocess.check_output("xinput create-master master", shell=True)
        self.master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True)
        # self.master_keyboard_id = subprocess.check_output("xinput list --id-only 'master keyboard'", shell=True)
        self.mouse_id = subprocess.check_output("xinput list --id-only 'mouse'", shell=True)
        # self.key_id = subprocess.check_output("xinput list --id-only 'key'", shell=True)

        subprocess.check_output(f"xinput reattach {self.mouse_id} {self.master_pointer_id}", shell=True)
        # subprocess.Popen(f"xinput reattach {key_id} {master_keyboard_id}", shell=True)

        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, Config.START_X)
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, Config.START_Y)
        self.mouse_ui.syn()


    def map_input(self, data):
        self.mouse_ui.write(data["type"], data["code"], data["val"])
        self.mouse_ui.syn()


    def map_input_abs(self, data):
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, data["x"])
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, data["y"])
        self.mouse_ui.syn()


#TODO: richtiges Mapping + !! mouse_handler wird zu oft/an falschen stellen aufgerufen