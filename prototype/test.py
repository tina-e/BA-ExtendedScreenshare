import time
import subprocess
from evdev import UInput, ecodes, AbsInfo, InputDevice

cap_mouse = {
    ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
    #ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
    ecodes.EV_ABS: [
        (ecodes.ABS_X, AbsInfo(value=0, min=0, max=4000, fuzz = 0, flat = 0, resolution = 31)),
        (ecodes.ABS_Y, AbsInfo(0, 0, 3000, 0, 0, 31)),
        (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 4000, 0, 0, 31))],
}

#cap_mouse = {
#    ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
#    ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
#}

mouse_ui = UInput(cap_mouse, name='mouse')

subprocess.check_output("xinput create-master master", shell=True)
master_pointer_id = subprocess.check_output("xinput list --id-only 'master pointer'", shell=True).strip().decode()
master_keyboard_id = subprocess.check_output("xinput list --id-only 'master keyboard'", shell=True).strip().decode()

mouse_id = subprocess.check_output(f"xinput list --id-only 'pointer:mouse'", shell=True).strip().decode()
subprocess.check_output(f"xinput reattach {mouse_id} {master_pointer_id}", shell=True)
time.sleep(20)

def map_mouse_movement(x, y):
    print(x, y)
    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, x)
    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, y)
    mouse_ui.syn()


#time.sleep(0.1)
#while True:

map_mouse_movement(100, 100)
time.sleep(0.006)
map_mouse_movement(550, 505)
time.sleep(0.006)
map_mouse_movement(1000, 1000)
time.sleep(0.006)
map_mouse_movement(505, 505)
time.sleep(0.006)
map_mouse_movement(100, 100)
time.sleep(0.006)
map_mouse_movement(505, 550)
time.sleep(0.006)
map_mouse_movement(1000, 1000)
time.sleep(0.006)
map_mouse_movement(550, 505)
time.sleep(0.006)
map_mouse_movement(100, 100)

#with UInput(cap_mouse, name='mouse') as mouse_ui:
    #print(mouse_ui.capabilities())

#    time.sleep(0.05)
#    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, 100)
#    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, 10)
#    mouse_ui.syn()

#print("Button.right".split('.')[1])

#mouse_device = InputDevice('/dev/input/event11')
#key_device = InputDevice('/dev/input/event3')
#print(mouse_device.name)