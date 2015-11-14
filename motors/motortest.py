# -*- coding: utf-8 -*-
from motors import motors
import time

# Pins are defined in the order: right 1 and 2 (IN1, IN2) and left 1 and 2 (IN3, IN4)
# ENA and ENB are optional for PWM, but not required
pinArray = [27, # IN1
            22, # IN2
            23, # IN3
            24, # IN4
            25, # ENA
            8]  # ENB
wheels = motors(pinArray)

wheels.spinCW() # Spin counter-clockwise for 2.5 seconds
time.sleep(2.5)
wheels.changeDC(50) # Slower speed for 2.5 seconds
time.sleep(2.5)

wheels.changeDC(100)

wheels.spinCCW()
time.sleep(2.5)
wheels.changeHz(50)
time.sleep(2.5)

wheels.forw()
time.sleep(5)

wheels.backw()
time.sleep(5)

wheels.stop()
wheels.quit()
