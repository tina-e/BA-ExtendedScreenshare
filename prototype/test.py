import time

from evdev import UInput, ecodes, AbsInfo

cap_mouse = {
    ecodes.EV_KEY: [ecodes.BTN_LEFT, ecodes.BTN_RIGHT],
    ecodes.EV_REL: [ecodes.REL_X, ecodes.REL_Y],
    ecodes.EV_ABS: [
        #(ecodes.ABS_X, AbsInfo(value=0, min=0, max=255, fuzz = 0, flat = 0, resolution = 0)),
        #(ecodes.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0)),
        (ecodes.ABS_MT_POSITION_X, (0, 128, 255, 0))],
}

with UInput(cap_mouse, name='mouse', version=0x3) as mouse_ui:
    while True:
        print(mouse_ui.capabilities())

        mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_MT_POSITION_X, 100)
        mouse_ui.write(ecodes.EV_ABS, ecodes.ABS_Y, 10)
        mouse_ui.syn()

        time.sleep(10)
