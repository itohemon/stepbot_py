from tb67s249 import TB67S249
import time
import utime

rightMotor = TB67S249( 7,  6,  5,  4,  3,  2, 1, 0)
leftMotor  = TB67S249(15, 14, 13, 12, 11, 10, 9, 8)

leftMotor.setRunMode("v")
leftMotor.setReset(False)
leftMotor.setTorque(True)
leftMotor.setStepSize(7)
leftMotor.setAgc(True)

rightMotor.setRunMode("v")
rightMotor.setReset(False)
rightMotor.setTorque(True)
rightMotor.setStepSize(7)
rightMotor.setAgc(True)

'''
leftMotor.start()
rightMotor.start()

leftMotor.setDir(True)
leftMotor.setStep(6400 * 2)
rightMotor.setDir(False)
rightMotor.setStep(6400 * 2)

for i in range(4):
    time.sleep(1)
    rightMotor.setDir(True)
    time.sleep(1)
    rightMotor.setDir(False)

time.sleep(5)

leftMotor.stop()
rightMotor.stop()
leftMotor.setTorque(False)
rightMotor.setTorque(False)
'''

leftMotor.setCCWRot(True)
rightMotor.setCCWRot(False)

leftMotor.start()
rightMotor.start()

for n in range(2):
    for i in range(30):
        step = i * 0.1
        leftMotor.setRPS(step)
        rightMotor.setRPS(step)
        print(step)
        utime.sleep_ms(10)

    time.sleep(1)

    for i in range(30):
        step = i * 0.1
        leftMotor.setRPS(3.0 - step)
        rightMotor.setRPS(3.0 - step)
        print(3.0 - step)
        utime.sleep_ms(10)
        
    leftMotor.setRPS(0)
    rightMotor.setRPS(0)
    time.sleep(1)

    for i in range(30):
        step = i * 0.1 * -1.0
        leftMotor.setRPS(step)
        rightMotor.setRPS(step)
        print(step)
        utime.sleep_ms(10)

    time.sleep(1)

    for i in range(30):
        step = i * 0.1 * -1.0
        leftMotor.setRPS(- 3.0 - step)
        rightMotor.setRPS(- 3.0 - step)
        print(3.0 - step)
        utime.sleep_ms(10)
        
    leftMotor.setRPS(0)
    rightMotor.setRPS(0)
    time.sleep(1)


leftMotor.setRPS(0)
rightMotor.setRPS(0)
leftMotor.setTorque(False)
rightMotor.setTorque(False)
