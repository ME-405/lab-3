# Cal Poly ME-405
## Lab 03
Jacob Bograd, Nick De Simone, Horacio Albarran

Documentation: https://me-405.github.io/lab-3/

---


This lab modifies our closed loop controller from Lab 02, which used to control the motor task's sampling rate with the 
use of blocking sleep statements. The controller has been updated to act as a generator function with a two-state FSM
controlling either data collection or printing. All blocking sleep commands were replaced with "yield", which allowed for 
task scheduling between closed loop control of the two motors. For this lab, one motor received a fixed Kp value of 0.6
while the other took its Kp from a serial input from the host computer. This second motor then sends its data back to the 
computer where it is graphed. Please refer to the graphs below for instances of proportional-control on this motor.  

NOTE: When the motor tasks are run at long intervals, the motors overshoot and produce uncontained oscillation. This causes
the microcontroller to run out of memory due to the amount of data it records, and subsequently fail to produce plotted data.



---
Graphs  
![Kp1](Images/Kp=1.png)  
This graphs shows the motor with a Kp of 1  
![Kp.5](Images/Kp=0.5.png)  
This graph shows the motor with a Kp of 0.5  
![Kp2.5](Images/Kp=0.5%5BSecond%5D.png)  
This graph shows the motor with a Kp of 0.5 again  
