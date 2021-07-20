import json
import subprocess
import time

from evdev import UInput, ecodes, AbsInfo, InputDevice
import Config

class EventHandlerEvdev():
    def __init__(self):
        self.cap_mouse = {
            #ecodes.EV_SYN: [ecodes.SYN_REPORT, ecodes.SYN_CONFIG, ecodes.SYN_MT_REPORT, ecodes.SYN_DROPPED, 21],
            ecodes.EV_KEY: [ecodes.KEY_POWER, ecodes.BTN_LEFT, ecodes.BTN_MOUSE, ecodes.BTN_RIGHT],
            #ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
            ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
            ecodes.EV_ABS: [
                (ecodes.ABS_X, AbsInfo(value=0, min=0, max=3600, fuzz = 0, flat = 0, resolution = 12)),
                (ecodes.ABS_Y, AbsInfo(value=0, min=0, max=2064, fuzz = 0, flat = 0, resolution = 12)),
                (ecodes.ABS_MT_ORIENTATION, AbsInfo(value=0, min=0, max=1, fuzz = 0, flat = 0, resolution = 0)),
                (ecodes.ABS_MT_POSITION_X, AbsInfo(value=0, min=0, max=3600, fuzz = 0, flat = 0, resolution = 0)),
                (ecodes.ABS_MT_POSITION_Y, AbsInfo(value=0, min=0, max=2064, fuzz = 0, flat = 0, resolution = 0)),
                (ecodes.ABS_MT_TOOL_X, AbsInfo(value=0, min=0, max=3600, fuzz = 0, flat = 0, resolution = 12)),
                (ecodes.ABS_MT_TOOL_Y, AbsInfo(value=0, min=0, max=2064, fuzz = 0, flat = 0, resolution = 12)),
                (ecodes.ABS_MT_TRACKING_ID, AbsInfo(0, 0, 65535, 0, 0, 0))],
        }

        self.cap_mouse = {
            ecodes.EV_KEY: [ecodes.KEY_POWER, ecodes.BTN_LEFT, ecodes.BTN_MOUSE, ecodes.BTN_RIGHT],
            # ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
            ecodes.EV_ABS: [
                (ecodes.ABS_X, AbsInfo(value=0, min=0, max=4000, fuzz=0, flat=0, resolution=31)),
                (ecodes.ABS_Y, AbsInfo(0, 0, 3000, 0, 0, 31)),
                (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 4000, 0, 0, 31))],
        }

        self.mouse_ui = UInput(self.cap_mouse, name='mouse', version=0x3)
        self.key_ui = UInput.from_device(Config.KEYBOARD_DEVICE_STREAMER, Config.MOUSE_DEVICE_STREAMER_CLICK, name='key')
        print(self.mouse_ui.capabilities(absinfo=True))
        print(self.key_ui.capabilities(absinfo=True))

        print(subprocess.check_output("xinput list", shell=True).decode('utf-8'))

        subprocess.check_output("xinput create-master master", shell=True)
        self.master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True).strip().decode()
        self.master_keyboard_id = subprocess.check_output("xinput list --id-only 'master keyboard'", shell=True).strip().decode()

        self.mouse_id = subprocess.check_output(f"xinput list --id-only 'pointer:mouse'", shell=True).strip().decode()
        self.click_id = subprocess.check_output(f"xinput list --id-only 'keyboard:mouse'", shell=True).strip().decode()
        self.scroll_id = subprocess.check_output(f"xinput list --id-only 'pointer:key'", shell=True).strip().decode()
        self.key_id = subprocess.check_output(f"xinput list --id-only 'keyboard:key'", shell=True).strip().decode()

        subprocess.check_output(f"xinput reattach {self.mouse_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.scroll_id} {self.master_pointer_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.click_id} {self.master_keyboard_id}", shell=True)
        subprocess.check_output(f"xinput reattach {self.key_id} {self.master_keyboard_id}", shell=True)

        print(subprocess.check_output("xinput list", shell=True).decode('utf-8'))


        #self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, Config.START_X)
        #self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, Config.START_Y)
        #self.mouse_ui.syn()

    def map_mouse_movement(self, x, y):
        print(x, y)
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, x+Config.START_X)
        self.mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, y+Config.START_Y)
        self.mouse_ui.syn()
        time.sleep(0.006)

    def map_mouse_click(self, x, y, button, was_pressed):
        return

    def map_mouse_scroll(self, dx, dy):
        return

    def map_keyboard(self, key, value):
        self.key_ui.write(ecodes.EV_KEY, key, value)
        self.key_ui.syn()

    def reattach_back(self):
        subprocess.check_output(f"xinput remove-master {self.master_pointer_id}", shell=True)

#TODO: richtiges Mapping -> Absolute Positionen???
#handler = EventHandlerEvdev()
#handler.map_mouse_movement(100, 100)
#handler.map_mouse_movement(550, 505)
#handler.map_mouse_movement(1000, 1000)
#handler.map_mouse_movement(505, 505)
#handler.map_mouse_movement(100, 100)
#handler.map_mouse_movement(505, 550)
#handler.map_mouse_movement(1000, 1000)
#handler.map_mouse_movement(550, 505)
#handler.map_mouse_movement(100, 100)
#subprocess.check_output(f"xinput remove-master 21", shell=True)

#{0: [0, 1, 2, 3, 21], 1: [272, 273], 2: [0, 1], 3: [(0, AbsInfo(value=0, min=0, max=4000, fuzz=0, flat=0, resolution=31)), (1, AbsInfo(value=0, min=0, max=3000, fuzz=0, flat=0, resolution=31)), (24, AbsInfo(value=0, min=0, max=4000, fuzz=0, flat=0, resolution=31))]}
#{0: [0, 1, 5, 21], 1: [116], 5: [0]}

#{('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('SYN_MT_REPORT', 2), ('SYN_DROPPED', 3), ('?', 21)], ('EV_KEY', 1): [(['BTN_LEFT', 'BTN_MOUSE'], 272), ('BTN_RIGHT', 273)], ('EV_REL', 2): [('REL_X', 0), ('REL_Y', 1)], ('EV_ABS', 3): [(('ABS_X', 0), AbsInfo(value=0, min=0, max=4000, fuzz=0, flat=0, resolution=31)), (('ABS_Y', 1), AbsInfo(value=0, min=0, max=3000, fuzz=0, flat=0, resolution=31)), (('ABS_PRESSURE', 24), AbsInfo(value=0, min=0, max=4000, fuzz=0, flat=0, resolution=31))]}
#{('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('?', 5), ('?', 21)], ('EV_KEY', 1): [('KEY_POWER', 116)], ('EV_SW', 5): [('SW_LID', 0)]}



#{0: [0, 1, 21], 1: [116]}
#ecodes.EV:SYN: [ecodes.SYN_REPORT, ecodes.SYNCONFIG, ecodes.SYN_MT_REPORT, ecodes.SYN_DROPPED, 21]
#ecodes.EV_KEY: [ecodes.KEY_POWER, [ecodes.BTN_LEFT, ecodes.BTN_MOUSE], ecodes.BTN_RIGHT]
#{0: [0, 1, 5, 21], 1: [116], 5: [0]}

#{('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('?', 21)], ('EV_KEY', 1): [('KEY_POWER', 116)]}
#{('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('?', 5), ('?', 21)], ('EV_KEY', 1): [('KEY_POWER', 116)], ('EV_SW', 5): [('SW_LID', 0)]}