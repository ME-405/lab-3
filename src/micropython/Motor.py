'''!
@file    Motor.py
@brief   MotorDriver class with associated methods 
@author  Nick De Simone, Jacob-Bograd, Horacio Albarran
@date	 January 30, 2022
'''

# Importing libraries
import pyb
from pyb import Pin
from pyb import ExtInt


class MotorDriver:
    
    def __init__(self, en_pin, in1pin, in2pin, inputTimer, channel1, channel2):
        '''!
        @brief     It will initialize the variables on the main file as well as motor defaults; MotorDriver-Class.

        '''
		
        # Initialize Motor 1 pins to be handled as PWM objects
        self.Pin1 = in1pin
        self.Pin2 = in2pin
        
        # Setting the timer variable to the timer object defined in the new.py file
        self.timer = inputTimer
        
        # Initialize the board's nSLEEP pin to be enabled
        self.enablePin = en_pin
        self.ch1 = self.timer.channel(channel1, pyb.Timer.PWM, pin=self.Pin1)
        self.ch2 = self.timer.channel(channel2, pyb.Timer.PWM, pin=self.Pin2)
        self.pinB2 = pyb.Pin(pyb.Pin.cpu.B2)
        #print("DEBUG: PIN1 ", self.Pin1, "\n PIN2", self.Pin2, "\n enPIN", self.enablePin)
        #print("DEBUG: ENABLED")
        
    def enable(self):
        '''!
        @brief    Enable the motor
        '''
        self.enablePin.high()
        #print("DEBUG: ENABLED")
        
    def disable(self):
        '''!
        @brief    Sets the motor duty for the motor to zero
        '''
        self.ch1.pulse_width_percent(0)
        self.ch2.pulse_width_percent(0)
        #print('DISABLING: Setting duty cycle to ' + str(0))
        
    def set_duty_cycle(self, duty):
        '''!
        @details Setting duty performance for the motor
        @param   Duty ranging from negative to positive one-hundred
        '''
		
        if duty >= 0:
            self.ch1.pulse_width_percent(duty)
            self.ch2.pulse_width_percent(0)
        #    print('MOTOR: Setting duty cycle to ' + str(duty))

        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(-duty)
        #    print('MOTOR: Setting duty cycle to NEGATIVE' + str(duty))

		
		
		
		