#!/usr/bin/env python

# Test Module for NOX : Noughts and crosses / Tic Tac Toe Game
# lights LED when reed switch closes

import sys
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_LED_Backpack")
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_GPIO")
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_PureIO")
sys.path.insert(0, "/home/pi/tictactoe/dependencies/Adafruit_Python_CharLCD")

# import smbus
import time
import math
from Adafruit_LED_Backpack import Matrix8x8
import RPi.GPIO as GPIO

# Call this only when there is a change. 
# i.e. curr_input and new_input are different.
def find_change(curr_input, new_input):
    assert curr_input != new_input

    for i in range(9):
        a = curr_input[i]
        b = new_input[i]

        if a>b:
            return "Close", i+1

        if a<b:
            return "Open", i+1

    raise Exception("Should not have come here")

#LED setup
# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8(address=0x70, busnum=1)
# check using I2cdetect -y 1  to make sure the address is 70, if not edit the line above to change it
# the correct address

# Initialize the display. Must be called once before using the display.
display.begin()
display.clear()
display.write_display()

print "starting"
# now look for a change
GPIO.setmode(GPIO.BCM)

# This is a list of GPIO pins connected to squares as numbered
# in the original project. 
gpio_list = [26, 19, 13, 6, 5, 22, 27, 17, 4]
for pin in gpio_list:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

curr_input = [1] * 9

# Loop until user presses CTRL-C
while True:
  new_input = [GPIO.input(x) for x in gpio_list]

  if curr_input != new_input:
    # There has been a state change.
    dirx, w = find_change(curr_input, new_input)

    x = int((w-1)/3)+1   # anodes numbers starts 1
    y = (2+w)%3   # cathodes number start 0

    print "x =", x, ", y =", y
      
    if dirx == "Close":   display.set_pixel(x, y, 1)  # switch on the LED
    if dirx == "Open":   display.set_pixel(x, y, 0)  # switch off the LED
        
    display.write_display()
    print "square", w, " Reed Switch " , dirx    # chcol[(w+2)%3], (int((w-1)/3))+1
    curr_input = new_input
      
  time.sleep(0.1)



