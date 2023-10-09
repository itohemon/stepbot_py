from tb67s249 import TB67S249
import time

rightMotor = TB67S249( 7,  6,  5,  4,  3,  2, 1, 0)
leftMotor  = TB67S249(15, 14, 13, 12, 11, 10, 9, 8)

leftMotor.setReset(False)
leftMotor.setTorque(True)
leftMotor.setStepSize(4)
leftMotor.setAgc(True)

rightMotor.setReset(False)
rightMotor.setTorque(True)
rightMotor.setStepSize(4)
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

leftMotor.setRPS(2.0)
rightMotor.setRPS(2.0)
time.sleep(3)
leftMotor.setRPS(-2.0)
rightMotor.setRPS(-2.0)
time.sleep(3)

leftMotor.setRPS(0)
rightMotor.setRPS(0)
'''
leftMotor.setTorque(False)
rightMotor.setTorque(False)
'''