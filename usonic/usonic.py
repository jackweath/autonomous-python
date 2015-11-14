def distance(TRIG, ECHO, setT=0):
    # Pin set up
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    try:
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
    except:
        print "ERROR when setting up pins"

    # Settling time
    # Optional variable, may affect accuracy
    time.sleep(setT)

    # A burst is sent
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Safety start notation
    startSig = time.time()

    # Noting when signal was sent
    while GPIO.input(ECHO) == 0:
      startSig = time.time()

    # Noting when signal was recieved
    while GPIO.input(ECHO) == 1:
      stopSig = time.time()

    # Calculating distance
    totalSig = stopSig - startSig
    sigDistance = totalSig * 34000
    sigDistance = sigDistance / 2

    # Resetting the GPIO pins for now
    GPIO.cleanup()

    # Returning relevant distance
    return sigDistance
