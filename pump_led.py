# in 1 = pump gpio 17 button = 16
# in 2 = LED gpio 27 button = 25

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

pump = 17
pump_button = 16

led = 27
led_button = 25

GPIO.setup(led, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(led_button, GPIO.IN)
GPIO.setup(pump_button, GPIO.OUT)
GPIO.output(led, 1)
GPIO.output(pump, 1)

while True:
    if GPIO.input(led_button) == 0:
        if GPIO.input(led) == 1:
            GPIO.output(led, 0)
            time.sleep(0.5)
        elif GPIO.input(led) == 0:
            GPIO.output(led, 1)
            time.sleep(0.5)


    if GPIO.input(pump_button) == 0:
        if GPIO.input(pump_button) == 0:
            GPIO.output(pump, 0)
            print("pump ON")
        else:
            GPIO.output(pump, 1)
    time.sleep(0.5)