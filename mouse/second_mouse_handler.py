# evdev
# UInput is used to create a virtual input device
import subprocess
import threading

import xinput

from evdev import UInput, ecodes as e
import time

# specify capabilities for our virtual input device
cap_mouse = {
    e.EV_REL: (e.REL_X, e.REL_Y),
    e.EV_KEY: (e.BTN_LEFT, e.BTN_RIGHT),
}

cap_key = {
    e.EV_KEY: (e.BTN_LEFT, e.BTN_RIGHT),
    e.EV_KEY: (e.KEY_A, e.KEY_E),
}


output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
print(output)

output = subprocess.check_output("xinput create-master accessor", shell=True)
print(output)

output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
print(output)


def handle_mouse():
    with UInput(cap_mouse, name="mouse") as mouse_ui, UInput(cap_key, name="key") as key_ui:
        output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
        print(output)
        #output = subprocess.check_output("xinput reattach 25", shell=True)
        #print(output)
        #output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
        #print(output)

        # click
        time.sleep(60) #TODO: programmatically reattach

        mouse_ui.write(e.EV_REL, e.REL_X, 1000)
        mouse_ui.syn()
        while True:
            mouse_ui.write(e.EV_REL, e.REL_X, 50)
            mouse_ui.syn()
            time.sleep(0.25)

            mouse_ui.write(e.EV_REL, e.REL_Y, 50)
            mouse_ui.syn()
            time.sleep(0.25)

            key_ui.write(e.EV_KEY, e.BTN_LEFT, 1)
            key_ui.syn()
            key_ui.write(e.EV_KEY, e.BTN_LEFT, 0)
            key_ui.syn()
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

handle_mouse()
#TODO: programmatically remove-master