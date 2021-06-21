import time

from evdev import UInput, ecodes, AbsInfo

cap_mouse = {
    ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
    #ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
    ecodes.EV_ABS: [
        (ecodes.ABS_X, AbsInfo(value=0, min=0, max=4000, fuzz = 0, flat = 0, resolution = 31)),
        (ecodes.ABS_Y, AbsInfo(0, 0, 3000, 0, 0, 31)),
        (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 4000, 0, 0, 31))],
}


with UInput(cap_mouse, name='mouse', version=0x3) as mouse_ui:
    print(mouse_ui.capabilities())

    time.sleep(60)
    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_X, 100)
    mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, 10)
    mouse_ui.syn()

