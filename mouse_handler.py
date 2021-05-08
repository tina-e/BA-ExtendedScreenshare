# evdev
# UInput is used to create a virtual input device
from evdev import UInput, ecodes as e
import time

# specify capabilities for our virtual input device
capabilities = {
    e.EV_REL: (e.REL_X, e.REL_Y),
    e.EV_KEY: (e.BTN_LEFT, e.BTN_RIGHT),
}


with UInput(capabilities) as device:
    # click
    time.sleep(1)
    device.write(e.EV_REL, e.REL_X, 100)
    device.syn()
    time.sleep(1)

    device.write(e.EV_REL, e.REL_Y, 500)
    device.syn()
    time.sleep(1)

    #device.write(e.EV_KEY, e.BTN_LEFT, 1)
    #device.syn()
    #time.sleep(0.01)

    # release
    #device.write(e.EV_KEY, e.BTN_LEFT, 0)
    #device.syn()






