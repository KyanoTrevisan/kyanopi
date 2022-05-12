import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
control_pins = [5,6,19,26]
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
GPIO.output(5,1)
GPIO.output(6,1)
GPIO.output(19,1)
GPIO.output(26,1)
