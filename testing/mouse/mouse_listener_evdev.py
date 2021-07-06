from evdev import InputDevice, ecodes, events, categorize, AbsInfo

device = InputDevice('/dev/input/event12')
#device = InputDevice('/dev/input/event3')
device._rawcapabilities.update({ecodes.EV_ABS: [
        (ecodes.ABS_X, AbsInfo(value=0, min=0, max=4000, fuzz = 0, flat = 0, resolution = 31)),
        (ecodes.ABS_Y, AbsInfo(0, 0, 3000, 0, 0, 31)),
        (ecodes.ABS_PRESSURE, AbsInfo(0, 0, 4000, 0, 0, 31))]})
print(device.capabilities(verbose=True, absinfo=False))
for event in device.read_loop():
    #print(event)
    #if isinstance(event, events.RelEvent):
    if event.type == ecodes.ABS_X:
        print(event)
    #if event.type == e.EV_KEY:
    #    print(categorize(event))
    #    print(event.code) #key
    #    print(event.value) #down=1, up=0, hold=2
    #    print("_____")
    #if event.type == e.EV_KEY:
    #      print("clicked")
