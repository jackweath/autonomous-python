import RPi.GPIO as GPIO
import time, sys

class newSensor:
    def __init__(self, TRIG, ECHO):
        self.TRIG = TRIG
        self.ECHO = ECHO

    def getDist(self, setT=0):
        # Pin set up
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        try:
            GPIO.setup(self.TRIG,GPIO.OUT)
            GPIO.setup(self.ECHO,GPIO.IN)
        except:
            print("ERROR when setting up pins", sys.exc_info()[0])
            raise

        # Settling time
        # Optional variable, may affect accuracy
        time.sleep(setT)

        # A burst is sent
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        # Safety start notation
        startSig = time.time()

        # Noting when signal was sent
        while GPIO.input(self.ECHO) == 0:
          startSig = time.time()

        # Noting when signal was recieved
        while GPIO.input(self.ECHO) == 1:
          stopSig = time.time()

        # Calculating distance
        totalSig = stopSig - startSig
        sigDistance = totalSig * 34000
        sigDistance = sigDistance / 2

        # Resetting the GPIO pins for now
        GPIO.cleanup()

        # Returning relevant distance
        return sigDistance

    
def cleanup():
    GPIO.cleanup()