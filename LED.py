# in 1 gpio5
# in 2 gpio6
# in 3 gpio19
# in 4 gpio26

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
control_pins = [5,6,19,26]
motor_turn = 20
motor_reverse = 21
GPIO.setup(motor_turn, GPIO.IN)
GPIO.setup(motor_reverse, GPIO.IN)
for pin in control_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

while True:
  if GPIO.input(motor_turn) == 0:
    for i in range(512):
      for halfstep in halfstep_seq[::1]:
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep[pin])
        time.sleep(0.001)
  if GPIO.input(motor_reverse) == 0:
    for i in range(512):
      for halfstep in halfstep_seq[::-1]:
        for pin in range(4):
          GPIO.output(control_pins[pin], halfstep[pin])
        time.sleep(0.001)