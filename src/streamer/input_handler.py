import errno
import subprocess
import time
# from wmctrl import Window
from event_types import get_device_by_button
from evdev import UInput, ecodes, AbsInfo, InputDevice


class InputHandler():
    '''
    This class handles the receiver's input performed inside the stream.
    These input events will be mapped to an independent input device created by evdev.
    '''
    def __init__(self, configurator):
        self.config = configurator
        self.cap_mouse = {
            ecodes.EV_KEY: [ecodes.KEY_POWER, ecodes.BTN_LEFT, ecodes.BTN_MOUSE, ecodes.BTN_RIGHT, ecodes.BTN_MIDDLE],
            ecodes.EV_REL: [ecodes.REL_WHEEL],
            ecodes.EV_ABS: [
                (ecodes.ABS_X, AbsInfo(value=0, min=0, max=self.config.RESOLUTION_X, fuzz=0, flat=0, resolution=31)),
                (ecodes.ABS_Y, AbsInfo(0, 0, self.config.RESOLUTION_Y, 0, 0, 31)),
                (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 4000, 0, 0, 31))],
        }
        self.mouse_ui = None
        self.key_ui = None

    def create_device(self):
        self.mouse_ui = UInput(self.cap_mouse, name='mouse', version=0x3)
        # Capabilities for the virtual keyboard are copied by the local keyboard plus mouse-buttons to allow clicks
        self.key_ui = UInput.from_device(InputDevice(self.config.KEYBOARD_DEVICE_PATH), InputDevice(self.config.MOUSE_DEVICE_PATH), name='key')

        subprocess.check_output("xinput create-master master", shell=True)
        self.master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True).strip().decode()
        self.master_keyboard_id = subprocess.check_output("xinput list --id-only 'master keyboard'", shell=True).strip().decode()

        self.mouse_id = subprocess.check_output(f"xinput list --id-only 'pointer:mouse'", shell=True).strip().decode()
        self.click_id = subprocess.check_output(f"xinput list --id-only 'keyboard:mouse'", shell=True).strip().decode()
        self.scroll_id = subprocess.check_output(f"xinput list --id-only 'pointer:key'", shell=True).strip().decode()
        self.key_id = subprocess.check_output(f"xinput list --id-only 'keyboard:key'", shell=True).strip().decode()

        # attaching the virtual input devices to new master to make them independent from the local input devices
        subprocess.check_output(f"xinput reattach {self.mouse_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.scroll_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.click_id} {self.master_keyboard_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.key_id} {self.master_keyboard_id}", shell=True)

        self.map_mouse_movement(0, 0)

    def map_mouse_movement(self, x, y):
        try:
            x = x + self.config.START_X
            y = y + self.config.START_Y
            self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, x)
            self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
            self.mouse_ui.syn()
            time.sleep(0.006) # required with abs positions
        # make sure the input device still exists to avoid input-mapping during closing the app
        except OSError as err:
            if err.errno == errno.EBADFD:
                return

    def map_mouse_click(self, x, y, button, was_pressed):
        self.mouse_ui.write(ecodes.EV_KEY, get_device_by_button(button), was_pressed)
        # synchronise only when key is released again or currently holded
        if not was_pressed: self.key_ui.syn()

    def map_mouse_scroll(self, dx, dy):
        self.mouse_ui.write(ecodes.EV_REL, ecodes.REL_WHEEL, dy)
        self.key_ui.syn()

    def map_keyboard(self, key, value):
        self.key_ui.write(ecodes.EV_KEY, key, value)
        # synchronise only when key is released again or currently holded
        if value != 1: self.key_ui.syn()

    def simulate_copy(self):
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 2)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_C, 1)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_C, 0)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
        self.key_ui.syn()

    def simulate_paste(self):
        print("test sim1")
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 1)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 2)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_V, 1)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_V, 0)
        self.key_ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTCTRL, 0)
        self.key_ui.syn()
        print("test sim2")

    '''def simulate_drop(self, x_drop, y_drop):
        dragon_win = Window.by_name('dragon')[0]
        x_drag = dragon_win.x + (dragon_win.w / 2)
        y_drag = dragon_win.y + (dragon_win.h / 2)

        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, x_drag)
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, y_drag)
        self.mouse_ui.syn()
        time.sleep(0.006)

        self.mouse_ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 1)
        self.mouse_ui.syn()

        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, x_drop)
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, y_drop)
        self.mouse_ui.syn()
        time.sleep(0.006)

        self.mouse_ui.write(ecodes.EV_KEY, ecodes.BTN_LEFT, 0)
        self.mouse_ui.syn()'''

    def remove_device(self):
        '''
        removes the second independent input device as soon as the receiver ends watching
        Avoids distracting mouse cursor when not needed
        '''
        self.mouse_ui.close()
        self.key_ui.close()
        subprocess.check_output(f"xinput remove-master {self.master_pointer_id}", shell=True)
