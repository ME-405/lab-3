'''! 
@file     main.py
@brief    File that runs the encoder and motor
@author   Nick De Simone, Jacob-Bograd, Horacio Albarran
@date     January 30, 2022
'''

# Importing libraries and classes
import utime
from Motor import MotorDriver
from encoder import Encoder
from closedLoopControl import closedLoopController as closed_loop
from pyb import Pin
import pyb

# Instantiated object for the encoder as well as timer,
encoderPin1 = pyb.Pin(pyb.Pin.board.PC6)
encoderPin2 = pyb.Pin(pyb.Pin.board.PC7)
EncTimer = 8
EncoderDriver = Encoder(encoderPin1, encoderPin2, EncTimer, 1, 2)

# Instantiated the objects for the chosen Motor,
motorEnable = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.IN, pyb.Pin.PULL_UP)
motorPin1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
motorPin2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
motorTimer = pyb.Timer(3, freq=20000)
Motor = MotorDriver(motorEnable, motorPin1, motorPin2, motorTimer, 1, 2)
utime.sleep_ms(10) #saftey
input_interval = 10
# input_interval = int(input("Enter the interval"))
clc = closed_loop(input_interval, EncoderDriver, Motor)
# print("about to enable the motor")
Motor.enable()
clc.control_algorithm()

def main():
    '''!
    @brief    This is the function that the Nucleo will run on boot
              It creates the closed loop controller object and runs the control algorithm
    '''
    utime.sleep_ms(10) #saftey
    input_interval = 10
    # input_interval = int(input("Enter the interval"))
    clc = closed_loop(input_interval, EncoderDriver, Motor)
    # print("about to enable the motor")
    Motor.enable()
    # print("just about to go into while")
    while True:
        try:
            #       print("starting the algorithm")
            clc.control_algorithm()
        except KeyboardInterrupt:
            Motor.disable()
            #       print("HIT THE EXCEPTION")
            break


print('out of loop')


if __name__ == '__main__':
   main()
