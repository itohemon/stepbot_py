from tb67s249 import TB67S249
import time

rightMotor = TB67S249( 7,  6,  5,  4,  3,  2, 1, 0)
leftMotor  = TB67S249(15, 14, 13, 12, 11, 10, 9, 8)

leftMotor.setReset(False)
leftMotor.setEnable(True)
leftMotor.setStepSize(1)
leftMotor.setAgc(False)
leftMotor.setDir(True)
leftMotor.setStep(700)

rightMotor.setReset(False)
rightMotor.setEnable(True)
rightMotor.setStepSize(1)
rightMotor.setAgc(False)
rightMotor.setDir(False)
rightMotor.setStep(700)

leftMotor.start()
rightMotor.start()

for i in range(4):
    time.sleep(1)
    rightMotor.setDir(True)
    time.sleep(1)
    rightMotor.setDir(False)

leftMotor.stop()
rightMotor.stop()
leftMotor.setEnable(False)
rightMotor.setEnable(False)
