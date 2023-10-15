import RPi.GPIO as GPIO
import math
import time
from controller_class import xbox_controller

# Initialize GPIO pins for motor control
GPIO.setmode(GPIO.BCM)
"""
                    WARNING
    GPIO Pin number is not the same as pin number
    For example: GPIO18 corresponds to Pin 12
    All pin definitions need to be with the GPIO pin number
"""
# Define GPIO pins for H-bridge motor driver
ENA = 12
IN1 = 5
IN2 = 6

ENB = 19
IN3 = 16
IN4 = 26

ENC = 14
IN5 = 15
IN6 = 18

END = 17
IN7 = 27
IN8 = 22

Servo_pin = 23
# Set GPIO pins as output
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENC, GPIO.OUT)
GPIO.setup(IN5, GPIO.OUT)
GPIO.setup(IN6, GPIO.OUT)
GPIO.setup(END, GPIO.OUT)
GPIO.setup(IN7, GPIO.OUT)
GPIO.setup(IN8, GPIO.OUT)
GPIO.setup(Servo_pin, GPIO.OUT)

# Initialize PWM instances for ENA, ENB, ENC and END
pwm_a = GPIO.PWM(ENA, 100)
pwm_b = GPIO.PWM(ENB, 100)
pwm_c = GPIO.PWM(ENC, 100)
pwm_d = GPIO.PWM(END, 100)
pwm_servo = GPIO.PWM(Servo_pin, 100)
"""-----------------------------------------------------------------"""
pwm_a.start(0)
pwm_b.start(0)
pwm_c.start(0)
pwm_d.start(0)
pwm_servo.start(0)
#Movement code below:
xbox = xbox_controller()
def stop_move():
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    pwm_c.ChangeDutyCycle(0)
    pwm_d.ChangeDutyCycle(0)
def speed_cal(x_axis, y_axis):
    speed = (math.sqrt(x_axis**2 + y_axis**2)/(math.sqrt(2) * 2**15)) * 100
    #speed = (abs(y_axis)/ (2**15)) * 100
    return speed
def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN5, GPIO.HIGH)
    GPIO.output(IN6, GPIO.LOW)
    GPIO.output(IN7, GPIO.HIGH)
    GPIO.output(IN8, GPIO.LOW)
    #pwm_a.ChangeDutyCycle(speed_cal(x_axis, y_axis))
    #pwm_b.ChangeDutyCycle(speed_cal(x_axis, y_axis))
    pwm_a.ChangeDutyCycle(25)
    pwm_b.ChangeDutyCycle(25)
    pwm_c.ChangeDutyCycle(25)
    pwm_d.ChangeDutyCycle(25)
def move_back():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    GPIO.output(IN5, GPIO.LOW)
    GPIO.output(IN6, GPIO.HIGH)
    GPIO.output(IN7, GPIO.LOW)
    GPIO.output(IN8, GPIO.HIGH)
    """pwm_a.ChangeDutyCycle(speed_cal(x_axis, y_axis))
    pwm_b.ChangeDutyCycle(speed_cal(x_axis, y_axis))
    pwm_c.ChangeDutyCycle(speed_cal(x_axis, y_axis))
    pwm_d.ChangeDutyCycle(speed_cal(x_axis, y_axis))"""
    pwm_a.ChangeDutyCycle(25)
    pwm_b.ChangeDutyCycle(25)
    pwm_c.ChangeDutyCycle(25)
    pwm_d.ChangeDutyCycle(25)
"""def control_rover(x_axis, y_axis):
    if (y_axis < -256):
        if (x_axis > -2048 and x_axis < 2048):
            move_forward
            time.sleep(0.01)
            stop_move()
    elif (y_axis > 256):
        if (x_axis > -2048 and x_axis < 2048):
            move_back
            time.sleep(0.01)
            stop_move()"""

def move_left():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN5, GPIO.HIGH)
    GPIO.output(IN6, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    pwm_b.ChangeDutyCycle(0)
    pwm_c.ChangeDutyCycle(50)
    pwm_d.ChangeDutyCycle(0)
def move_right():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    GPIO.output(IN7, GPIO.HIGH)
    GPIO.output(IN8, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(50)
    pwm_c.ChangeDutyCycle(0)
    pwm_d.ChangeDutyCycle(50)
def control_rover(x_axis, y_axis, right_x_axis, right_y_axis):
    if (y_axis < -512):
        if (x_axis > -2048 and x_axis < 2048):
            move_forward()
            time.sleep(0.1)
            stop_move()
    elif (y_axis > 512):
        if (x_axis > -2048 and x_axis < 2048):
            move_back()
            time.sleep(0.1)
            stop_move()
    elif (y_axis > -512 or y_axis < 512):
        if (x_axis < -2048):
            move_left()
            time.sleep(0.1)
            stop_move()
        elif (x_axis > 2048):
            move_right()
            time.sleep(0.1)
            stop_move()

    if (right_x_axis == 0):
        pwm_servo.ChangeDutyCycle(15)
        #time.sleep(1)
    elif (right_x_axis < -(2**6)):
        pwm_servo.ChangeDutyCycle(2.5)
        time.sleep(0.5)
    elif (right_x_axis > (2**6)):
        pwm_servo.ChangeDutyCycle(24)
        time.sleep(0.5)

#Main Function Below:
def main():
    
    while(True):
        x_axis, y_axis, right_x, right_y = xbox.get_analog()
        control_rover(x_axis, y_axis, right_x, right_y)
if __name__ == '__main__':
    main()
