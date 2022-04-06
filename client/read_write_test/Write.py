#!/usr/bin/env python

import RPi.GPIO as GPIO
from rfid_library import SimpleMFRC522

board = SimpleMFRC522(bus=0, device=0)  # plytka blizej przycisku
board2 = SimpleMFRC522(bus=0, device=1)  # plytka dalej od przycisku

try:
    text = input('New data:')
    print("Now place your tag to write")
    board.write(text)
    print("Written")
    text = input('New data:')
    print("Now place your tag to write")
    board2.write(text)
    print("Written")
finally:
    GPIO.cleanup()
