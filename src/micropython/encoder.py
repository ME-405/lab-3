"""! 
@file     encoder.py
@brief    A driver for reading from Quadrature Encoders
@author   Nick De Simone, Jacob-Bograd, Horacio Albarran
@date     January 30, 2022
"""

## Importing libraries
import pyb


class Encoder:
    '''! 
		@brief       Interface with quadrature encoders
        @details     Initializes encoder objects and implements 
						methods to work directly with encoder hardware
    '''

    def __init__(self, pin1, pin2, timer, channel1, channel2):
        '''! 
			@brief   Encoder Driver to manipulate physical encoders
            @details Constructs encoder objects by linking specified
						encoder numbers to corresponding Nucleo pins
            @param   pin1 specify first pin of the encoder
            @param   pin2 specify second pin of the encoder
            @param   timer specify the chosen timer number for the encoder
            @param   channel1 specify the first chosen channel
            @param   channel2 specify the second chosen channel
        '''
		
        # Establish Period for Encoder Counting, 2^16 - 1, used to correct for overflow
        self.period = 65535
        
        # Setting pin parameters to instance variables
        self.pin1 = pin1
        self.pin2 = pin2
        
        # Instantiated timer and channel objects
        self.timer = pyb.Timer(timer, prescaler = 0, period = self.period)
        self.ch1 = self.timer.channel(channel1, pyb.Timer.ENC_AB, pin=self.pin1)
        self.ch2 = self.timer.channel(channel2, pyb.Timer.ENC_AB, pin=self.pin2)
        
        # Reference count used to compute change in encoder position (delta)
        # ref_count will update in each run through the "update" method
        self.ref_count = 0
        
        # Current Position: Position in [ticks] of the associated encoder
        # current_pos will update in each run through the "update" method       
        self.current_pos = 0
        self.delta = 0
        
    def update(self):
        '''! 
		@details     Provides with the updated position provided by the chosen encoder and delta value
        '''
        # Actualizing the encoder position 
        self.update_count = self.timer.counter()
        #print("DEBUG: UPDATE COUNT = ", str(self.update_count))
        
        # Obtaining the difference between the encoder positions
        self.delta = self.update_count - self.ref_count
        #print("DEBUG: Delta value = ", str(self.delta))
        
        # Correcting for overflow and underflow of the encoder reader value
        if self.delta > 0 and self.delta > self.period/2:
            self.delta -= self.period
        if self.delta < 0 and abs(self.delta) > self.period/2:
            self.delta += self.period

        # Setting the reference position based on the "current" encoder position
        self.ref_count = self.update_count
        
        # Updating the current position based on the provided delta value
        self.current_pos += self.delta
     
    def read(self):
        '''! 
			@brief      Retrieve encoder position in [ticks]
            @details    Returns encoder position at time of function call
            @return     current_pos
        '''
        #print('Current position is = ' + str(self.current_pos))
        return self.current_pos

    def set_position(self, position):
        '''! 
			@brief      Set position in [ticks] of encoder
            @param      position The new position of the encoder shaft
        '''   
        self.current_pos = position

    def zero(self):
        '''! 
			@brief      Allow user to set position in [ticks] of encoder to zero
        '''
        self.current_pos = 0
        #print('Position: '+ str(self.current_pos))

    def get_delta(self):
        '''! 
			@brief      Return difference in encoder position in [ticks]
            @details    Returns change in encoder position between time of 
							function call and previous encoder update
            @return     The change in position of the encoder shaft
							between the two most recent updates
        '''
        return self.delta
		
		
		
		
		
		
		
		
		