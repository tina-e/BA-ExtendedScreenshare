import threading

from evdev import UInput, ecodes as e
import time
import subprocess

capabilities = {
    e.EV_REL: (e.REL_X, e.REL_Y),
    e.EV_KEY: (e.BTN_LEFT, e.BTN_RIGHT),
}

mouse_ui = UInput(capabilities)
key_ui = UInput()

output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
print(output)

output = subprocess.check_output("xinput create-master accessor", shell=True)
print(output)

output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
print(output)

time.sleep(30)

mouse_ui.write(e.EV_REL, e.REL_X, 1000)
mouse_ui.syn()
while True:
    mouse_ui.write(e.EV_REL, e.REL_X, 50)
    mouse_ui.syn()
    time.sleep(0.25)

    mouse_ui.write(e.EV_REL, e.REL_Y, 50)
    mouse_ui.syn()
    time.sleep(0.25)

    mouse_ui.write(e.EV_KEY, e.BTN_LEFT, 1)
    mouse_ui.syn()
    mouse_ui.write(e.EV_KEY, e.BTN_LEFT, 0)
    mouse_ui.syn()

    key_ui.write(e.EV_KEY, e.KEY_E, 1)
    key_ui.syn()
    key_ui.write(e.EV_KEY, e.KEY_E, 0)
    key_ui.syn()
    time.sleep(0.25)

    mouse_ui.write(e.EV_REL, e.REL_X, -50)
    mouse_ui.syn()
    time.sleep(0.25)

    mouse_ui.write(e.EV_REL, e.REL_Y, -50)
    mouse_ui.syn()
    time.sleep(0.25)
