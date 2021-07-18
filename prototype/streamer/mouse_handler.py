import json
import subprocess
import time

from evdev import UInput, ecodes, AbsInfo

import Config

class EventHandlerEvdev():
    def __init__(self):
        self.cap_mouse = {
            ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
            ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
            ecodes.EV_ABS: [
                (ecodes.ABS_X, AbsInfo(value=0, min=0, max=4000, fuzz = 0, flat = 0, resolution = 31)),
                (ecodes.ABS_Y, AbsInfo(0, 0, 3000, 0, 0, 31)),
                (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 4000, 0, 0, 31))],
        }

        self.mouse_ui = UInput(self.cap_mouse, name='mouse', version=0x3)
        self.key_ui = UInput.from_device(Config.KEYBOARD_DEVICE_STREAMER, Config.MOUSE_DEVICE_STREAMER_CLICK, name='key')
        print(subprocess.check_output("xinput list", shell=True))

        subprocess.check_output("xinput create-master master", shell=True)
        self.master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True).strip().decode()
        self.master_keyboard_id = subprocess.check_output("xinput list --id-only 'master keyboard'", shell=True).strip().decode()

        self.mouse_id = subprocess.check_output(f"xinput list --id-only 'mouse'", shell=True).strip().decode()
        self.scroll_id = subprocess.check_output(f"xinput list --id-only 'pointer:mouse'", shell=True).strip().decode()
        self.click_id = subprocess.check_output(f"xinput list --id-only 'keyboard:mouse'", shell=True).strip().decode()
        self.key_id = subprocess.check_output(f"xinput list --id-only 'key'", shell=True).strip().decode()

        subprocess.check_output(f"xinput reattach {self.mouse_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.scroll_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.click_id} {self.master_keyboard_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.key_id} {self.master_keyboard_id}", shell=True)
        print(subprocess.check_output("xinput list", shell=True))

        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, Config.START_X)
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, Config.START_Y)
        self.mouse_ui.syn()

    def map_mouse_movement(self, x, y):
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, x)
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
        self.mouse_ui.syn()

    def map_mouse_click(self, x, y, button, was_pressed):
        return

    def map_mouse_scroll(self, dx, dy):
        return

    def map_keyboard(self, key, value):
        self.key_ui.write(ecodes.EV_KEY, key, value)
        self.key_ui.syn()


#TODO: richtiges Mapping -> Absolute Positionen???