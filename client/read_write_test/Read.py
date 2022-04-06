#!/usr/bin/env python

from rfid_library import SimpleMFRC522
import RPi.GPIO as GPIO

board = SimpleMFRC522(bus=0, device=0)  # plytka blizej przycisku
board2 = SimpleMFRC522(bus=0, device=1)  # plytka dalej od przycisku

try:
    id, text = board.read()
    print(id)
    print(text)
    id, text = board2.read()
    print(id)
    print(text)
finally:
    GPIO.cleanup()
