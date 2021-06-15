from evdev import InputDevice, ecodes as e, events

device = InputDevice('/dev/input/event11')
print(device)
for event in device.read_loop():
    #if isinstance(event, events.RelEvent):
    print(event.type)
    if event.type == e.EV_KEY:
        print("clicked")
