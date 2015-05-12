#!/usr/bin/env python

import time

import RPi.GPIO as GPIO

def check_input(pin_num):
    GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        print GPIO.input(pin_num)
        time.sleep(1)

def find_change(curr_input, new_input):
    for i in range(9):
        a = curr_input[i]
        b = new_input[i]

        if a>b:
            return "Close", i+1

        if a<b:
            return "Open", i+1

    raise Exception("Should not have come here")

GPIO.setmode(GPIO.BCM)

# This is a list of GPIO pins connected to squares as numbered
# in the original project. 
gpio_list = [26, 19, 13, 12, 5, 22, 27, 17, 4]
for pin in gpio_list:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

curr_input = [1] * 9

while True:
    new_input = [GPIO.input(x) for x in gpio_list]
    # new_input[3] = 1 - new_input[3]
    # print "curr: ", curr_input
    # print "new: ", new_input
    if curr_input != new_input:
        # There has been a state change.
        dirx, square_num = find_change(curr_input, new_input)

        print "square", square_num, " Reed Switch " , dirx
        curr_input = new_input

    time.sleep(0.1)
    # raw_input("Enter: ")





    
