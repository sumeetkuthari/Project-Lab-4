import evdev
import time

class xbox_controller:
    
    def __init__(self):
        #self.controller = self.init_controller() #Instantiating the controller.
        self.controller = self.init_controller() 
        self.left_analog_x = 0 #Class will carry the left analog values
        self.left_analog_y = 0
        self.right_analog_x = 0
        self.right_analog_y = 0

    def init_controller(self): #Initializing the controller
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            print("Device is: {}".format(device.name))
            if 'Microsoft X-Box 360 pad' in device.name: 
                return device
        raise IOError('Microsoft X-Box 360 pad')
    
    def get_analog(self):
        event = self.controller.read_one()
        while event is not None:
            if event.type == evdev.ecodes.EV_ABS:
                if event.code == evdev.ecodes.ABS_X:
                    self.left_analog_x = event.value
                elif event.code == evdev.ecodes.ABS_Y:
                    self.left_analog_y = event.value
                elif event.code == evdev.ecodes.ABS_Z:
                    self.right_analog_x = event.value
                elif event.code == evdev.ecodes.ABS_Z:
                    self.right_analog_y = event.value
            event = self.controller.read_one()
        return self.left_analog_x, self.left_analog_y, self.right_analog_x, self.right_analog_y

if __name__ == '__main__':
    myXbox = xbox_controller()
    while(True):
        x_axis, y_axis, right_x, right_y = myXbox.get_analog()
        print("Left X: {}, Left Y: {}, Right X: {}, Right Y: {}".format(x_axis, y_axis, right_x, right_y))
        time.sleep(0.01)