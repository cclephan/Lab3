# Lab 3 Step Responses
## Christian Clephan, Kyle McGrath

Graphs below demonstrate two motors whose priority using cotask.py were both set equal and Kp = 0.35.
Periods of each motor were changed to find optimum value where the motors weren't unstable. The setpoint
value for each motor was 1 revolution (8,192 ticks).

![alt text](https://github.com/cclephan/Lab3/blob/main/Images/M1Period10.png?raw=true)

Figure 1: Step Response of Motor 1 at 10ms Period

This graph shows motor 1 at a 10ms period. The response shows the system is second order with some slight
overshoot, but the response is stable.

![alt text](https://github.com/cclephan/Lab3/blob/main/Images/M2Period10.png?raw=true)

Figure 2: Step Response of Motor 2 at 10ms Period

This graph shows motor 2 at a 10ms period. The response shows the system is second order with some slight
overshoot, but the response is stable.

![alt text](https://github.com/cclephan/Lab3/blob/main/Images/M1Period25.png?raw=true)

Figure 3: Step Response of Motor 1 at 25ms Period

This graph shows motor 1 at a 25ms period. The response shows the system overshoot and become unstable as
the motor oscillates around our setpoint value.

![alt text](https://github.com/cclephan/Lab3/blob/main/Images/M2Period25.png?raw=true)

Figure 4: Step Response of Motor 2 at 25ms Period

This graph shows motor 2 at a 25ms period. The response shows the system overshoot and oscillate for 
about 1 second and become stable around 1.3 seconds. Interesting that everything within software is the
same for both motors, yet one is stable and one is unstable at 25ms. This could be due to friction within
individual motors.

![alt text](https://github.com/cclephan/Lab3/blob/main/Images/Run3Period35.png?raw=true)

Figure 5: Step Response of Motor 2 at 35ms Period

This graph shows motor 2 at a 35ms period. The response shows the system overshoot and become unstable as
the motor oscillates around our setpoint value. 

A bug/feature within our program causes the motors to continue running after one step response until the
Nucleo board is reset TWICE. 
