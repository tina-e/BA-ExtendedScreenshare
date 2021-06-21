import json
import subprocess
import time

from evdev import UInput, ecodes, AbsInfo

import Config

class CustomInputDevice():
    def __init__(self):
        #self.cap_mouse = {
        #    ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
        #    ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
        #}

        self.cap_mouse = {
            ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
            #ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
            ecodes.EV_ABS: [
                (ecodes.ABS_X, AbsInfo(value=0, min=0, max=4000, fuzz = 0, flat = 0, resolution = 31)),
                (ecodes.ABS_Y, AbsInfo(0, 0, 3000, 0, 0, 31)),
                (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 4000, 0, 0, 31))],
        }

        self.mouse_ui = UInput(self.cap_mouse, name='mouse', version=0x3)
        # self.key_ui = UInput(self.cap_key, name="key")
        print(subprocess.check_output("xinput list", shell=True))

        subprocess.check_output("xinput create-master master", shell=True)
        self.master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True).strip().decode()
        print(self.master_pointer_id)
        # self.master_keyboard_id = subprocess.check_output("xinput list --id-only 'master keyboard'", shell=True)
        self.mouse_id = subprocess.check_output("xinput list --id-only 'mouse'", shell=True).strip().decode()
        print(self.mouse_id)
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


#TODO: richtiges Mapping -> Absolute Positionen???