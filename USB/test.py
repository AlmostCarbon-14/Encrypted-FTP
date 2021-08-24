#!/usr/bin/env python3 

import RPi.GPIO as GPIO
import time

led = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

for i in range(10):
    GPIO.output(led, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(led, GPIO.LOW)
    time.sleep(4)
    print("ran {} time(s)".format(i))
GPIO.cleanup()
