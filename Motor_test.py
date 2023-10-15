import RPi.GPIO as GPIO
import time

# Pin numbers for motor control
ENA = 12
IN1 = 16
IN2 = 18

ENB = 11
IN3 = 13
IN4 = 15

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Create PWM instances
pwma = GPIO.PWM(ENA, 100)
pwmb = GPIO.PWM(ENB, 100)

# Start PWM with 0% duty cycle
pwma.start(0)
pwmb.start(0)

def move_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwma.ChangeDutyCycle(50)
    pwmb.ChangeDutyCycle(50)

def move_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwma.ChangeDutyCycle(50)
    pwmb.ChangeDutyCycle(50)

def turn_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwma.ChangeDutyCycle(25)
    pwmb.ChangeDutyCycle(25)

def turn_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwma.ChangeDutyCycle(25)
    pwmb.ChangeDutyCycle(25)

while True:
    move_forward()
    time.sleep(2)
    move_backward()
    time.sleep(2)
    turn_left()
    time.sleep(2)
    turn_right()
    time.sleep(2)
