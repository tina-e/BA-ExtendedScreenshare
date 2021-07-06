import subprocess
from evdev import UInput, ecodes, AbsInfo
import pyautogui
import Config

class EventHandler:
    def __init__(self):
        self.mouse_ui = UInput.from_device(Config.MOUSE_DEVICE_STREAMER_POINT, Config.MOUSE_DEVICE_STREAMER_CLICK, name='mouse')
        self.key_ui = UInput.from_device(Config.KEYBOARD_DEVICE_STREAMER, Config.MOUSE_DEVICE_STREAMER_CLICK, name="key")
        print(subprocess.check_output("xinput list", shell=True))

        subprocess.check_output("xinput create-master master", shell=True)
        self.master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True).strip().decode()
        self.master_keyboard_id = subprocess.check_output("xinput list --id-only 'master keyboard'", shell=True).strip().decode()

        self.mouse_id = subprocess.check_output(f"xinput list --id-only '{Config.MOUSE_DEVICE_STREAMER_POINT.name}'", shell=True).strip().decode()
        self.scroll_id = subprocess.check_output(f"xinput list --id-only 'pointer:{Config.MOUSE_DEVICE_STREAMER_CLICK.name}'", shell=True).strip().decode()
        self.click_id = subprocess.check_output(f"xinput list --id-only 'keyboard:{Config.MOUSE_DEVICE_STREAMER_CLICK.name}'", shell=True).strip().decode()
        self.key_id = subprocess.check_output(f"xinput list --id-only '{Config.KEYBOARD_DEVICE_STREAMER.name}'", shell=True).strip().decode()

        subprocess.check_output(f"xinput reattach {self.mouse_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.scroll_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.click_id} {self.master_keyboard_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.key_id} {self.master_keyboard_id}", shell=True)
        print(subprocess.check_output("xinput list", shell=True))

    def map_mouse_movement(self, x, y):
        pyautogui.moveTo(x + Config.START_X, y + Config.START_Y)

    def map_mouse_click(self, x, y, button, was_pressed):
        if was_pressed:
            pyautogui.mouseDown(x + Config.START_X, y + Config.START_Y, button=str(button).split('.')[1])
        else:
            pyautogui.mouseUp(x + Config.START_X, y + Config.START_Y, button=str(button).split('.')[1])

    def map_mouse_scroll(self, dx, dy):
        pyautogui.scroll(dy)

    def map_keyboard(self, key, value):
        self.key_ui.write(ecodes.EV_KEY, key, value)
        self.key_ui.syn()

    def reattach_back(self):
        standard_master_pointer_id = subprocess.check_output("xinput list --id-only 'Virtual core pointer", shell=True).strip().decode()
        standard_master_keyboard_id = subprocess.check_output("xinput list --id-only 'Virtual core keyboard", shell=True).strip().decode()
        subprocess.check_output(f"xinput reattach {self.mouse_id} {standard_master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.scroll_id} {standard_master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.click_id} {standard_master_keyboard_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.key_id} {standard_master_keyboard_id}", shell=True)
