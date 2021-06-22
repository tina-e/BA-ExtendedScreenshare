import subprocess
from evdev import UInput, ecodes, AbsInfo
import pyautogui
import Config

class MouseHandler:
    def __init__(self):
        self.cap_mouse = {
            ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
            ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
        }

        self.mouse_ui = UInput(self.cap_mouse, name='mouse')
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

    def map_mouse_movement(self, x, y):
        pyautogui.moveTo(x, y)

    #def map_mouse_click(self, x, y):

    #def map_mouse_scroll(self, dx, dy):