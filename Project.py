from datetime import datetime
import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM) 
# Pin numbers
control_pins = [5,6,19,22]
motor_turn = 20
motor_reverse = 21
TRIG = 3
ECHO = 2
pump = 17
pump_button = 16
led = 27
led_button = 25


# Pin Setups
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

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(led, GPIO.OUT)
GPIO.setup(pump, GPIO.OUT)
GPIO.setup(led_button, GPIO.IN)
GPIO.setup(pump_button, GPIO.OUT)
GPIO.output(led, 1)
GPIO.output(pump, 1)


# LCD setup
# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
# Initialize display
dc = digitalio.DigitalInOut(board. D23) # data/command
cs1 = digitalio.DigitalInOut(board.CE1) # chip select CE1 for display
reset = digitalio.DigitalInOut(board.D24) # reset
display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate= 1000000)
display.bias = 4
display.contrast = 60
display.invert = True
# Clear the display. Always call show after changing pixels to make the display update visible!

# LCD text
txt_light = ""
txt_pump = ""

# intervals
feeding_time = "10:30:00"
lights_on = "18:00:00"
lights_off = "23:00:00"

# main

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # depth
    GPIO.output(TRIG, False)
    time.sleep(0.2)
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
        
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start    
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("Distance: ",distance,"cm")


    # pump and led
    if GPIO.input(pump) == 0:
        txt_pump = "ON"
        print("Pump On")
    else:
        txt_pump = "OFF"
        print("Pump Off")
    if GPIO.input(led) == 0:
        txt_light = "ON"
        print("LED On")
    else:
        txt_light = "OFF"
        print("LED Off")
    
    # pump
    if distance > 5:
        GPIO.output(pump, 0)
    else:
        GPIO.output(pump, 1)
    if GPIO.input(pump_button) == 0:
        if GPIO.input(pump_button) == 0:
            GPIO.output(pump, 0)
        else:
            GPIO.output(pump, 1)

    # LED
    if current_time == lights_on:
        GPIO.output(led, 0)
    elif current_time == lights_off:
        GPIO.output(led, 1)
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
            
        else:
            GPIO.output(pump, 1)
    time.sleep(0.5)

    # StepperMotor
    if current_time == feeding_time:
        for i in range(512):
            for halfstep in halfstep_seq[::1]:
                for pin in range(4):
                    GPIO.output(control_pins[pin], halfstep[pin])
                    time.sleep(0.001)
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
    display.fill(0)
    display.show()
    # Load default font.
    font = ImageFont.load_default()
    #font=ImageFont.truetype("/usr/share/fonts/truetype/freefo nt/Free SansBold.ttf", 10)
    # Get drawing object to draw on image
    image = Image.new('1', (display.width, display.height))
    draw = ImageDraw.Draw(image)
    # Draw a white filled box to clear the image.
    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)

    display.fill(0)
    draw.text((1,0),"Light " + txt_light, font=font)
    draw.text((1,8),"Pump "+ txt_pump, font=font)
    draw.text((1,16),"Depth "+ str(round(distance, 2)), font=font)
    draw.text((1, 24),"Time "+ str(current_time), font=font)
    display.image(image)
    display.show()
