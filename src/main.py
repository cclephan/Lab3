"""!
@file main.py
    This file contains two tasks, which each run a motor at a specific period and priority.
    Each motor task first initializes pins and creates encoder, motor, and controller objects.
    
    

@author Christian Clephan
@author Kyle McGrath
@date   2022-Feb-3
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
    Task which puts things into a share and a queue.
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
        #encoderShare.put (encoder.read())
        #motorShare.put()
        if start:
            encoder.zero()
            #Asks for a proportional gain value from user
            #Kp = float(input('Input a proportional gain value and press enter: '))
            #print('Start')
            #Instantiates controller object with specified Kp

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
            #utime.sleep_ms(10)
            
            #After 2 seconds from the start of the step response...
        if t_cur >= startTime+1000:
            #Printing out and resetting values for another step response
            start = True
            controller.i = True
            for n in range(len(controller.times)):
                print("{:}, {:}".format(controller.times[n],controller.motorPositions[n]))
                yield(0)
            controller.times = []
            controller.motorPositions = []
            startTime = utime.ticks_ms()
            encoder.zero()
            #Stop contiditon for user interface
            #print('Stop')
            motor.set_duty_cycle(0)
            

        yield (0)


def task2_fun ():
    """!
    Task which takes things out of a queue and share to display.
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
        #encoderShare.put (encoder.read())
        #motorShare.put()
        if start:
            encoder2.zero()
            #Asks for a proportional gain value from user
            #Kp = float(input('Input a proportional gain value and press enter: '))
            #print('Start')
            #Instantiates controller object with specified Kp

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
            #utime.sleep_ms(10)
            
            #After 2 seconds from the start of the step response...
        if t_cur >= startTime+1000:
            #Printing out and resetting values for another step response
            start = True
            controller2.i = True
            for n in range(len(controller2.times)):
                print("{:}, {:}".format(controller2.times[n],controller2.motorPositions[n]))
                yield 0
            controller2.times = []
            controller2.motorPositions = []
            startTime = utime.ticks_ms()
            encoder2.zero()
            #Stop contiditon for user interface
            #print('Stop')
            motor2.set_duty_cycle(0)
            

        yield (0)



# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print ('\033[2JTesting ME405 stuff in cotask.py and task_share.py\r\n'
           'Press ENTER to stop and show diagnostics.')

    # Create a share and a queue to test function and diagnostic printouts
    encoderShare = task_share.Share ('h', thread_protect = False, name = "Encoder Share")
    motorShare = task_share.Share ('h', thread_protect = False, name = "Motor Share")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task (task1_fun, name = 'Task_1', priority = 1, 
                         period = 10, profile = True, trace = False)
    task2 = cotask.Task (task2_fun, name = 'Task_2', priority = 1, 
                         period = 10, profile = True, trace = False)
    cotask.task_list.append (task1)
    #cotask.task_list.append (task2)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    #task1_fun()
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched ()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    #Something could be bogging down the system causing the system to overcompensate and run faster
    
    # Print a table of task data and a table of shared information data
    print ('\n' + str (cotask.task_list))
    print (task_share.show_all ())
    print (task1.get_trace ())
    print ('\r\n')
