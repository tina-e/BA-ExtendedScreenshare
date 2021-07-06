from evdev import InputDevice, ecodes as e, events, categorize

#device = InputDevice('/dev/input/event11')
device = InputDevice('/dev/input/event3')
print(device)
for event in device.read_loop():
    #if isinstance(event, events.RelEvent):
    if event.type == e.EV_KEY:
        print(categorize(event))
        print(event.code) #key
        print(event.value) #down=1, up=0, hold=2
        print("_____")
    #if event.type == e.EV_KEY:
    #      print("clicked")
