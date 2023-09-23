from machine import Pin
import time

TactSW1 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
TactSW2 = machine.Pin(23, machine.Pin.IN, machine.Pin.PULL_UP)
TactSW3 = machine.Pin(24, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if TactSW1.value() == 1:
        print("TactSW1 ON")
    else:
        print("TactSW1 OFF")

    if TactSW2.value() == 1:
        print("TactSW2 ON")
    else:
        print("TactSW2 OFF")

    if TactSW3.value() == 1:
        print("TactSW3 ON")
    else:
        print("TactSW3 OFF")

    time.sleep(0.1)