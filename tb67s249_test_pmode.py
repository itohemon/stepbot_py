from tb67s249 import TB67S249
import time
import math

rightMotor = TB67S249( 7,  6,  5,  4,  3,  2, 1, 0)
leftMotor  = TB67S249(15, 14, 13, 12, 11, 10, 9, 8)

leftMotor.setRunMode("p")
leftMotor.setReset(False)
leftMotor.setTorque(True)
leftMotor.setStepSize(1)
leftMotor.setAgc(True)
leftMotor.setCCWRot(True)

rightMotor.setRunMode("p")
rightMotor.setReset(False)
rightMotor.setTorque(True)
rightMotor.setStepSize(1)
rightMotor.setAgc(True)
rightMotor.setCCWRot(False)

r = 25
steps = int(1000 / (2.0 * r * math.pi) * 200)

for n in range(4):
    for i in range(steps):
        leftMotor.setForwardStep()
        rightMotor.setForwardStep()

    time.sleep(1)

    for i in range(100):
        leftMotor.setForwardStep()
        rightMotor.setReverseStep()

    time.sleep(1)
