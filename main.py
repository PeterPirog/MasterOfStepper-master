import time
import pyfirmata2
import serial
import Motor

board = pyfirmata2.Arduino('COM4')
print(board)
# DirPinMotor2 = 10
# StepPinMotor2 = 11
DirPinMotor2 = board.get_pin('d:10:o')
StepPinMotor2 = board.get_pin('d:11:o')
MinDelayMotor2 = 0.001  # us

print('Kierunek prawo')
DirPinMotor2.write(1)  # Kierunek prawo
tempDelay = MinDelayMotor2
for i in range(0, 1600):
    StepPinMotor2.write(1)
    # time.sleep(0.001)
    StepPinMotor2.write(0)
    # time.sleep(0.0001)

print('Kierunek lewo')
DirPinMotor2.write(0)  # Kierunek lewo
for i in range(0, 1600):
    StepPinMotor2.write(1)
    # time.sleep(0.0001)
    StepPinMotor2.write(0)
    # time.sleep(0.00001)

print('FINISH')
