#!/usr/bin/env python

import sys
import time

# print sys.path

from Adafruit_LED_Backpack import Matrix8x8

# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8(address=0x70, busnum=1)


# check using I2cdetect -y 1  to make sure the address is 70, if not edit the line above to change it
# the correct address
# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()
display.clear()

x = int(sys.argv[1]) # Anode
y = int(sys.argv[2]) # Cathode
display.set_pixel(x, y, 1)

# Write the display buffer to the hardware.  This must be called to
# update the actual display LEDs
display.write_display()

print "Waiting for 10 seconds..."
time.sleep(10)
display.set_pixel(x, y, 0)
display.write_display()
display.clear()
