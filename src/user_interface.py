"""!
@file user_interface.py
This file contains the user interface which will run on the PC and send serial
input to the Nucleo and read back serial output. Two motors will spin 1 revolution
at proportional gains and periods specified in main.py. Plots out graphs of step 
responses for each motor after a few seconds.
@author Christian Clephan
@author Kyle McGrath
@date   09-Feb-2022
@copyright (c) 2022 released under CalPoly
"""

import serial
from matplotlib import pyplot


with serial.Serial ('COM4', 115200) as s_port:
    #Enter to main.py to run step response
    s_port.write (b'\r\n')
    line = s_port.readline()
    time1 = []
    position1 = []
    time2 = []
    position2 = []
    #Reads through lines of main.py from Nucleo until it finds Stop
    while not b'EndM2' in line:
        try:
            temp = line.split (b',')
            if b'M1' in line:
                time1.append(float(temp[1]))
                position1.append(float(temp[2]))
            if b'M2' in line:
                time2.append(float(temp[1]))
                position2.append(float(temp[2]))
            #Appends to time and position lists
            
            
        except IndexError as error:
            print(error, line)
            #print(line)
            pass
        except ValueError as error:
            print(error, line)
        finally:
            line = s_port.readline()
    s_port.write(b'\x03')
    #Plotting both graphs
    pyplot.plot(time1, position1)
    pyplot.xlabel('Time (ms)')
    pyplot.ylabel('Position (ticks)')
    pyplot.grid(True)
    pyplot.title('Motor 1')
    pyplot.show()
    
    pyplot.plot(time2, position2)
    pyplot.xlabel('Time (ms)')
    pyplot.ylabel('Position (ticks)')
    pyplot.grid(True)
    pyplot.title('Motor 2')
    pyplot.show()

    