import time
from evdev import UInput, InputDevice
import uinput

def main():
    events = (
        uinput.ABS_X,
        uinput.ABS_Y,
        uinput.ABS_PRESSURE,
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        )

    with uinput.Device(events) as device:
        device.emit(uinput.ABS_X, 5)
        device.emit(uinput.ABS_Y, 5)
        time.sleep(1)
        device.emit(uinput.ABS_X, 50, syn=False)
        device.emit(uinput.ABS_Y, 50)
        time.sleep(1)
        device.emit(uinput.ABS_X, 5, syn=False)
        device.emit(uinput.ABS_Y, 5)
        time.sleep(1)
        device.emit(uinput.ABS_X, 50, syn=False)
        device.emit(uinput.ABS_Y, 50)

if __name__ == "__main__":
    #main()
    TOUCHSCREEN = InputDevice('/dev/input/event7')
    print(TOUCHSCREEN.capabilities(verbose=True))