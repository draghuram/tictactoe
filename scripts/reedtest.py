#!/usr/bin/env python

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    print GPIO.input(6)
    time.sleep(1)
