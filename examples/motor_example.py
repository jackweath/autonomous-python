# -*- coding: utf-8 -*-
from motors import motorSet
import time

# Pins are defined in the order: right 1 and 2 (IN1, IN2) and left 1 and 2 (IN3, IN4)
# ENA and ENB are optional for PWM, but not required
pinArray = [11, # IN1
            0, # IN2
            5, # IN3
            6, # IN4
            9, # ENA
            13]  # ENB
wheels = motorSet(pinArray)

wheels.spinLeft(100) # Spin counter-clockwise for 2.5 seconds
time.sleep(2.5)
wheels.spinLeft(50) # Slower speed for 2.5 seconds
time.sleep(2.5)

wheels.spinRight(100)
time.sleep(2.5)

wheels.spinRight(50)
time.sleep(2.5)

wheels.fwd(50)
time.sleep(5)

wheels.bwd(50)
time.sleep(5)

wheels.stop()
wheels.cleanup()
