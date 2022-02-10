"""!
@file main.py
    This file contains two tasks, which each run a motor at a specific period and priority.
    Each motor task first initializes pins and creates encoder, motor, and controller objects.

@author Christian Clephan
@author Kyle McGrath
@date   09-Feb-2022
@copyright (c) 2022 released under CalPoly
"""

import gc
import pyb
import cotask
import task_share
import encoder_clephan_mcgrath
import motor_clephan_mcgrath
import control
import utime

def task1_fun ():
    """!
    @brief Creates motor/encoder/controller 1 objects to run motor for step response
    @details First, pins are created that will be used in the encoder/motor driver
    and an encoder/motor object is created for the 2nd motor. The code then goes through a loop
    asking the user for a Kp value, running the response by constantly updating
    controller calculated duty and encoder position. After 2 seconds the encoder
    is set to zero and all information collected in time/position arrays is
    displayed. The user can exit the loop by pressing control+c, which will also
    turn off the motor.
    """
    m1_Kp = .35
    ticks_per_rev = 8192
    pinA10 = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_PP)
    pinB4 = pyb.Pin(pyb.Pin.board.PB4)
    pinB5 = pyb.Pin(pyb.Pin.board.PB5)
    pinC6 = pyb.Pin(pyb.Pin.board.PC6)
    pinC7 = pyb.Pin(pyb.Pin.board.PC7)
    encoder = encoder_clephan_mcgrath.Encoder(pinC6,pinC7,8)
    motor = motor_clephan_mcgrath.MotorDriver(pinA10, pinB4, pinB5, 3)
    controller = control.ClosedLoop([m1_Kp,0,0], [-100,100], ticks_per_rev)
    start = True
    
    while True:

        if start:
            encoder.zero()

            #Starting time to collect data
            startTime = utime.ticks_ms()
            t_cur = utime.ticks_ms()
            start = False
        else:
            #Updates encoder position, uses that value to update duty from controller, and sleeps 10ms
            encoder.update()
            t_cur = utime.ticks_ms()
            duty = controller.update(encoder.read(), startTime)
            motor.set_duty_cycle(duty)
            
            
            #After 2 seconds from the start of the step response...
        if t_cur >= startTime+2000:
            #Printing out and resetting values for another step response
            start = True
            controller.i = True
            for n in range(len(controller.times)):
                print("M1, {:}, {:}".format(controller.times[n],controller.motorPositions[n]))
                yield(0)
            controller.times = []
            controller.motorPositions = []
            startTime = utime.ticks_ms()
            encoder.zero()
            motor.set_duty_cycle(0)
            

        yield (0)


def task2_fun ():
    """!
    @brief Creates motor/encoder/controller 2 objects to run motor for step response
    @details First, pins are created that will be used in the encoder/motor driver
    and an encoder/motor object is created for the 2nd motor. The code then goes through a loop
    asking the user for a Kp value, running the response by constantly updating
    controller calculated duty and encoder position. After 2 seconds the encoder
    is set to zero and all information collected in time/position arrays is
    displayed. The user can exit the loop by pressing control+c, which will also
    turn off the motor.
    """
    m2_Kp = .35
    ticks_per_rev = 8192
    pinC1 = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
    pinA0 = pyb.Pin(pyb.Pin.board.PA0)
    pinA1 = pyb.Pin(pyb.Pin.board.PA1)
    pinB6 = pyb.Pin(pyb.Pin.board.PB6)
    pinB7 = pyb.Pin(pyb.Pin.board.PB7)
    encoder2 = encoder_clephan_mcgrath.Encoder(pinB6,pinB7,4)
    motor2 = motor_clephan_mcgrath.MotorDriver(pinC1, pinA0, pinA1, 5)
    controller2 = control.ClosedLoop([m2_Kp,0,0], [-100,100], ticks_per_rev)
    start = True
    
    while True:
        if start:
            encoder2.zero()

            #Starting time to collect data
            startTime = utime.ticks_ms()
            t_cur = utime.ticks_ms()
            start = False
        else:
            #Updates encoder position, uses that value to update duty from controller, and sleeps 10ms
            encoder2.update()
            t_cur = utime.ticks_ms()
            duty = controller2.update(encoder2.read(), startTime)
            motor2.set_duty_cycle(duty)
            
            #After 2 seconds from the start of the step response...
        if t_cur >= startTime+2000:
            #Printing out and resetting values for another step response
            start = True
            controller2.i = True
            for n in range(len(controller2.times)):
                print("M2, {:}, {:}".format(controller2.times[n],controller2.motorPositions[n]))
                yield 0
            print('EndM2')
            controller2.times = []
            controller2.motorPositions = []
            startTime = utime.ticks_ms()
            encoder2.zero()
            #Stop contiditon for user interface
            #print('Stop')
            motor2.set_duty_cycle(0)
            

        yield (0)



if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')
    
    input('Press enter to begin program')

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 1, 
                         period = 35, profile = True, trace = False)
    cotask.task_list.append (task1)
    cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    while True:
         try:
             cotask.task_list.pri_sched ()
         except KeyboardInterrupt:
             break

    # Empty the comm port buffer of the character(s) just pressed
    #Something could be bogging down the system causing the system to overcompensate and run faster
    
    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
