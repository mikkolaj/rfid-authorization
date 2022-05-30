from threading import Thread
from time import sleep
import RPi.GPIO as GPIO


DOOR_LED_PIN = 17
UNAUTHORIZED_PIN = 27


class Door(Thread):
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DOOR_LED_PIN, GPIO.OUT)
        GPIO.output(DOOR_LED_PIN, GPIO.LOW)
        GPIO.setup(UNAUTHORIZED_PIN, GPIO.OUT)
        GPIO.output(UNAUTHORIZED_PIN, GPIO.LOW)

    def open(self):
        for _ in range(10):
            GPIO.output(DOOR_LED_PIN, GPIO.HIGH)
            sleep(0.05)
            GPIO.output(DOOR_LED_PIN, GPIO.LOW)
            sleep(0.05)

    def close(self):
        for _ in range(5):
            GPIO.output(DOOR_LED_PIN, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(DOOR_LED_PIN, GPIO.LOW)
            sleep(0.1)

    def indicate_unauthorized_access(self):
        for _ in range(10):
            GPIO.output(UNAUTHORIZED_PIN, GPIO.HIGH)
            sleep(0.05)
            GPIO.output(UNAUTHORIZED_PIN, GPIO.LOW)
            sleep(0.05)
