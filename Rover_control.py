import RPi.GPIO as GPIO
import xbox

# Initialize GPIO pins for motor control
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins for H-bridge motor driver
ENA = 11
IN1 = 13
IN2 = 15
ENB = 12
IN3 = 16
IN4 = 18
ENC = 29
IN5 = 31
IN6 = 33
END = 32
IN7 = 36
IN8 = 38

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

# Initialize PWM instances for ENA, ENB, ENC and END
pwm_a = GPIO.PWM(ENA, 100)
pwm_b = GPIO.PWM(ENB, 100)
pwm_c = GPIO.PWM(ENC, 100)
pwm_d = GPIO.PWM(END, 100)

# Initialize Xbox controller
joy = xbox.Joystick()

# Define function to control the movement of the rover
def control_rover(x_axis, y_axis):
    left_speed = y_axis + x_axis
    right_speed = y_axis - x_axis
    
    # Set the direction of the front motors
    if left_speed > 0:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    
    # Set the direction of the back motors
    if right_speed > 0:
        GPIO.output(IN7, GPIO.HIGH)
        GPIO.output(IN8, GPIO.LOW)
    else:
        GPIO.output(IN7, GPIO.LOW)
        GPIO.output(IN8, GPIO.HIGH)
    
    # Set the speed of the front motors
    if abs(left_speed) > 32767:
        left_speed = 32767
    pwm_a.start(abs(left_speed))
    pwm_b.start(abs(left_speed))
    
    # Set the speed of the back motors
    if abs(right_speed) > 32767:
        right_speed = 32767
    pwm_c.start(abs(right_speed))
    pwm_d.start(abs(right_speed))

# Continuously read the values from the left analog stick and control the rover
try:
    while True:
        x_axis, y_axis = joy.leftStick()
        control_rover(x_axis, y_axis)
except KeyboardInterrupt:
    joy.close()
    GPIO.cleanup()
