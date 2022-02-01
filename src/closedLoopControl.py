"""!
@file    closedLoopControl.py
@details Close loop control runs and manages data interaction produced by the hardware 
@author  Nick De Simone, Jacob-Bograd, Horacio Albarran
@date    January 30, 2022
"""

# Importing the required classes and libraries
from Motor import MotorDriver
from encoder import Encoder
from pyb import Pin
from pyb import UART
import pyb
import time
import utime

class closedLoopController:
    def __init__(self, input_interval, encoder, MotorDriver):
        '''!
		@brief   closedLoopController manages the data provided by the encoder as well as running calculations
        @details This files manages the data provided by the encoder, it also manages the
					 setting values for the proper functioning of the motor, and any other
					 required calculations for the motor to work properly
        @param   input_interval provides with the desired interval to collect data
		@param   encoder set the parameter given for the chosen encoder
		@param   motor provides with the chosen motor
        '''

        # Setting some parameters
        self.final_point = 0
        self.kp = 0
        self.current_time = 0
        self.gain = 0  # the gain will be updated in a function
        self.encoder = encoder
        self.motor = MotorDriver
        self.start_time = utime.ticks_ms()  # the staring time
        self.interval = input_interval  # the interval of the milliseconds
        self.nextTime = utime.ticks_add(self.start_time, self.interval)
		
		# Setting the UART for serial communication
        self.uart = UART(2)
        self.uart.init(115200)
		
		# Setting arrays to store data
        self.time_list = []
        self.encoder_list = []

    def control_algorithm(self):
		'''!
        @details It manages the value for kp as well as setting different
					parameters for the duty cycle of the motor based on the 
					actuation value; which is dependent of the difference 
					encoder positions as well as the value of kp
		'''

		self.kp = float(input())
		self.final_point = 16384
		self.encoder.set_position(0)  # zero out the encoder value
        # print("values set")
		while True:
			self.encoder.update()  # update the encoder value
			error = self.final_point - self.encoder.current_pos  # get the error
            # print("error = ", error)
			if error == 0:
				# print("DEBUG: ERROR IS NOW 0")
				self.motor.disable()  # disable the motor
				break

			else:
				self.current_time = utime.ticks_ms()
				if utime.ticks_diff(self.current_time, self.nextTime) >= 0:
					voltage = 3.3                          # Voltage used for the microcontroller
					actuation = (error * self.kp)/voltage  # get the actuation
					if actuation >= 80:
						self.motor.set_duty_cycle(80)
					elif 30 >= actuation > 5:
						self.motor.set_duty_cycle(30)
					elif -30 <= actuation < 5:
						self.motor.set_duty_cycle(-30)
					elif actuation <= -80:
						self.motor.set_duty_cycle(-80)
					elif -5 <= actuation <= 5:
                        #        print("DEBUG: I HAVE FINISHED")
						self.motor.disable()
						break
					else:
						self.motor.set_duty_cycle(actuation)
				self.update_list()  # update the list position\
				utime.sleep_ms(self.interval)
                #self.nextTime = utime.ticks_add(self.nextTime, self.interval)  # update the next time

		self.print_list()  # print out the list when we are done

    def update_setpoint(self):
		'''!
        @details It sets the desired position of the encoder in ticks 
					as defined by the input of the user
		'''
		self.final_point = int(input("Please enter the setpoint"))

    def update_interval(self):
		'''!
        @details It defines the interval at which data from the encoder 
					will be collected as defined by the input of the user
		'''
		self.interval = int(input("Please enter the interval"))

    def update_list(self):
		'''!
        @details It updates the encoder position and the current time-stamp while
					also appending such values to the corresponding array
		'''
		
		
		# Updating encoder's position on ticks
		self.encoder.update()
		#self.Position = float(self.Data[2])
		encoder_value = self.encoder.current_pos
		
		# Updating the time-stamp 
		timestamp = utime.ticks_diff(utime.ticks_ms(), self.start_time)
		
		# Appending values to the corresponding array
		self.time_list.append(timestamp)
		self.encoder_list.append(encoder_value)

		# print("DEBUG: ", timestamp, encoder_value)

    def update_kp(self):
		'''!
        @details It ask for the user's input for the variable kp 
		'''
        #self.kp = float(input("Please enter kp"))
		
		#print('\r\n')
		#print('Allowed K_p values are from 0-1')
        #print('and press "S" to provide with a new command while collecting data')
        #print(' "P" to plot the data, and "S" to start collecting data from zero')
		self.K_p = input('Provide with input for K_p:  ')
		
    def print_list(self):
		'''!
        @details It provides with the numerical values for the encoder positions as 
					well as the corresponding time-stamp to such encoder position
		'''
		data = zip(self.time_list, self.encoder_list)
		for numbers in data:
			print(*numbers)
		print("DONE")
		
        # clear the different lists
		self.time_list.clear()
		self.encoder_list.clear()

    def input_kp(self):
		'''!
			@details This functions is used for the computer interface interaction 
		'''
		while self.uart.any == 0:
			utime.sleep_us(50)
		self.kp = self.uart.read()
	
	
	
	
	
	
	
	
	
