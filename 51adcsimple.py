import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac = [8,11,7,1,0,5,12,6]
comp = 14
troyka = 13
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT,initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]
def adc():
    for value in range(256):
        GPIO.output(dac,decimal2binary(value))
        time.sleep(0.01)
        if GPIO.input(comp) == 1:
            return value
    return value
try:
    while(True):
        value = adc()
        v = value*3.3/256
        print(value,v)
finally:
    GPIO.output(dac,0)