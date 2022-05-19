from threading import Thread
from time import sleep
import RPi.GPIO as GPIO


DOOR_LED_PIN = 17


class Door(Thread):
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DOOR_LED_PIN, GPIO.OUT)
        GPIO.output(DOOR_LED_PIN, GPIO.LOW)
        pass

    def open(self):
        for _ in range(10):
            GPIO.output(DOOR_LED_PIN, GPIO.HIGH)
            sleep(0.05)
            GPIO.output(DOOR_LED_PIN, GPIO.LOW)
            sleep(0.05)

        pass

    def close(self):
        for _ in range(5):
            GPIO.output(DOOR_LED_PIN, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(DOOR_LED_PIN, GPIO.LOW)
            sleep(0.1)
        pass
