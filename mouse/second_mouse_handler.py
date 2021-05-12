# evdev
# UInput is used to create a virtual input device
import subprocess
import threading

from evdev import UInput, ecodes as e
import time

# specify capabilities for our virtual input device
capabilities = {
    e.EV_REL: (e.REL_X, e.REL_Y),
    e.EV_KEY: (e.BTN_LEFT, e.BTN_RIGHT),
}


output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
print(output)

output = subprocess.check_output("xinput create-master accessor", shell=True)
print(output)

output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
print(output)


def handle_mouse():
    with UInput(capabilities) as mouse_ui:
        output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
        print(output)
        output = subprocess.check_output("xinput reattach 25", shell=True)
        print(output)
        output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
        print(output)

        # click
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
            time.sleep(0.25)

            mouse_ui.write(e.EV_REL, e.REL_X, -50)
            mouse_ui.syn()
            time.sleep(0.25)

            mouse_ui.write(e.EV_REL, e.REL_Y, -50)
            mouse_ui.syn()
            time.sleep(0.25)

def handle_keyboard():
    with UInput() as device_key:
        output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
        print(output)
        output = subprocess.check_output("xinput reattach 25 26", shell=True)
        print(output)
        output = subprocess.check_output("xinput list", shell=True).decode("utf-8")
        print(output)

        device_key.write(e.EV_REL, e.REL_X, 1000)
        device_key.syn()
        while True:
            device_key.write(e.EV_KEY, e.KEY_E, 1)
            device_key.syn()
            device_key.write(e.EV_KEY, e.KEY_E, 0)
            device_key.syn()
            time.sleep(0.5)

try:
    #threading.Thread(target=handle_mouse).start()
    #threading.Thread(target=handle_keyboard).start()
    handle_mouse()
    handle_keyboard()
except KeyboardInterrupt:
    pass

subprocess.check_output("xinput remove-master 25", shell=True)
subprocess.check_output("xinput remove-master 26", shell=True)