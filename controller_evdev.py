import evdev
import time
left_analog_x = 0
left_analog_y = 0
def init_controller():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print("Device is: {}".format(device))
        if 'Microsoft X-Box 360 pad' in device.name:
            return device
    raise IOError('Microsoft X-Box 360 pad')

def get_left_analog_stick(controller):
    global left_analog_x 
    global left_analog_y
    event = controller.read_one()
    while event is not None:
        if event.type == evdev.ecodes.EV_ABS:
            if event.code == evdev.ecodes.ABS_X:
                left_analog_x = event.value
            elif event.code == evdev.ecodes.ABS_Y:
                left_analog_y = event.value
        event = controller.read_one()
    return (left_analog_x, left_analog_y)

def main():
    controller = init_controller()
    while True:
        left_analog_stick = get_left_analog_stick(controller)
        print(f"Left Analog Stick: ({left_analog_stick[0]}, {left_analog_stick[1]})")
        time.sleep(0.01)

if __name__ == '__main__':
    main()


