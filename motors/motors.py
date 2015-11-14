# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

class motors:
    pinArray = []
    def __init__(self, pinArray):
        # Pass pin array to class
        self.pinArray = pinArray

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Setup each pin in the array
        for i in range(4):
            GPIO.setup(pinArray[i], GPIO.OUT)
            GPIO.output(pinArray[i], False)

        # 6 stated pins are required for PWM use
        if len(pinArray) == 6:
            GPIO.setup(pinArray[4], GPIO.OUT)
            GPIO.setup(pinArray[5], GPIO.OUT)
            GPIO.output(pinArray[4], True)
            GPIO.output(pinArray[5], True)
            # Set up pin for PWM at 100Hz
            # Using public member variables to be accessed in class
            self.PWMLeft = GPIO.PWM(self.pinArray[4], 100)
            self.PWMRight = GPIO.PWM(self.pinArray[5], 100)

            # 100% initial duty cycle
            self.PWMLeft.start(100)
            self.PWMRight.start(100)



    # Functions for each wheel movement
    def rightBack(self):
        GPIO.output(self.pinArray[0], True)
        GPIO.output(self.pinArray[1], False)

    def rightFor(self):
        GPIO.output(self.pinArray[0], False)
        GPIO.output(self.pinArray[1], True)

    def leftBack(self):
        GPIO.output(self.pinArray[2], True)
        GPIO.output(self.pinArray[3], False)

    def leftFor(self):
        GPIO.output(self.pinArray[2], False)
        GPIO.output(self.pinArray[3], True)

    # End user functions
    def spinCW(self):
        self.leftFor()
        self.rightBack()

    def spinCCW(self):
        self.leftBack()
        self.rightFor()

    def backw(self):
        self.leftBack()
        self.rightBack()

    def forw(self):
        self.leftFor()
        self.rightFor()

    def leftSpeed(self, speed):
        self.PWMLeft.ChangeDutyCycle(speed)

    def rightSpeed(self, speed):
        self.PWMRight.ChangeDutyCycle(speed)

    # Changing the duty cycle means the percentage of the freq that the pulse is HIGH for
    # Changes DC for both motors
    def changeDC(self, duty=100):
        self.leftSpeed(duty)
        self.rightSpeed(duty)

    # Allows users to change the frequency from the default 100Hz
    # Changes frequency for both motors
    def changeHz(self, freq=100):
        self.PWMLeft.ChangeFrequency(freq)
        self.PWMRight.ChangeFrequency(freq)

    # Stops wheel movement
    def stop(self):
        for i in range(4):
            GPIO.output(self.pinArray[i], False)

    # Tidies and closes GPIO pin usage
    def quit(self):
        self.stop()
        self.PWMLeft.stop()
        self.PWMRight.stop()
        GPIO.cleanup()
        print "Pins stopped and cleaned"
