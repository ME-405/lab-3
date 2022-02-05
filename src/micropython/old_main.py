'''! 
@file     old_main.py
@brief    File that runs the encoder and motor
@author   Nick De Simone, Jacob-Bograd, Horacio Albarran
@date     January 30, 2022
'''

# Importing libraries and classes
import utime
from Motor import MotorDriver
from encoder import Encoder
from closedLoopControl import ClosedLoopController as closed_loop
from pyb import Pin
import pyb
import gc
import cotask
import task_share

# Instantiated object for the encoder as well as timer,
encoderPin1 = pyb.Pin(pyb.Pin.board.PC6)
encoderPin2 = pyb.Pin(pyb.Pin.board.PC7)
EncTimer1 = 8
EncoderDriver1 = Encoder(encoderPin1, encoderPin2, EncTimer1, 1, 2)

# Instantiated the objects for the chosen Motor,
motorEnable1 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.IN, pyb.Pin.PULL_UP)
motor1Pin1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
motor1Pin2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
motorTimer = pyb.Timer(3, freq=20000)
Motor1 = MotorDriver(motorEnable1, motor1Pin1, motor1Pin2, motorTimer, 1, 2)
utime.sleep_ms(10)  # saftey
input_interval = 10
# input_interval = int(input("Enter the interval"))
clc1 = closed_loop(input_interval, EncoderDriver1, Motor1)

# Instantiated object for the encoder as well as timer,
encoder2Pin1 = pyb.Pin(pyb.Pin.board.PB6)
encoder2Pin2 = pyb.Pin(pyb.Pin.board.PB7)
EncTimer2 = 4
EncoderDriver2 = Encoder(encoder2Pin1, encoder2Pin2, EncTimer2, 1, 2)

# Instantiated the objects for the chosen Motor,
motorEnable2 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.IN, pyb.Pin.PULL_UP)
motor2Pin1 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP)
motor2Pin2 = pyb.Pin(pyb.Pin.board.PB1, pyb.Pin.OUT_PP)
# motorTimer2 = pyb.Timer(3, freq=20000)
Motor2 = MotorDriver(motorEnable2, motor2Pin1, motor2Pin2, motorTimer, 3, 4)
utime.sleep_ms(10)  # saftey
input_interval = 10
# input_interval = int(input("Enter the interval"))
clc2 = closed_loop(input_interval, EncoderDriver2, Motor2)

# print("about to enable the motor")
Motor1.enable()


# clc1.control_algorithm()


def main():
    '''!
    @brief    This is the function that the Nucleo will run on boot
              It creates the closed loop controller object and runs the control algorithm
    '''
    utime.sleep_ms(10)  # saftey
    # print("about to enable the motor")
    Motor1.enable()
    # print("just about to go into while")
    while True:
        try:
            #       print("starting the algorithm")
            clc1.control_algorithm()
            clc2.control_algorithm()
        except KeyboardInterrupt:
            Motor1.disable()
            #       print("HIT THE EXCEPTION")
            break


def task1_fun():
    """!
    Task which puts things into a share and a queue.
    """
    counter = 0
    while True:
        share0.put(counter)
        q0.put(counter)
        counter += 1

        yield (0)


def task2_fun():
    """!
    Task which takes things out of a queue and share to display.
    """
    while True:
        # Show everything currently in the queue and the value in the share
        print("Share: {:}, Queue: ".format(share0.get()), end='');
        while q0.any():
            print("{:} ".format(q0.get()), end='')
        print('')

        yield (0)


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print('\0332Welcome to the closed loop controller\r\n')

    # Create a share and a queue to test function and diagnostic printouts
    share0 = task_share.Share('h', thread_protect=False, name="Share 0")
    q0 = task_share.Queue('L', 16, thread_protect=False, overwrite=False,
                          name="Queue 0")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(clc1.control_algorithm(), name='clc1', priority=1,
                        period=400, profile=True, trace=False)
    task2 = cotask.Task(clc2.control_algorithm(), name='clc2', priority=2,
                        period=1500, profile=True, trace=False)
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any
    # character is received through the serial port
    vcp = pyb.USB_VCP()
    while not vcp.any():
        cotask.task_list.pri_sched()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read()
    # Print a table of task data and a table of shared information data
    print('\n' + str(cotask.task_list))
    print(task_share.show_all())
    print(task1.get_trace())
    print('\r\n')
