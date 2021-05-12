from evdev import InputDevice, ecodes as e

device = InputDevice('/dev/input/event11')
print(device)
for event in device.read_loop():
    print()
    if event.type == e.EV_KEY:
        print("clicked")
