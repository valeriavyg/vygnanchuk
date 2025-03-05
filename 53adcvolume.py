import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
dac = [8,11,7,1,0,5,12,6]
leds = [2,3,4,17,27,22,10,9]
comp = 14
troyka = 13
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(leds,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT,initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
def b2d(a): 
    res = 0
    s = 128
    for i in range(8):
        res += a[i]*s
        s /= 2
    return res
def adc():
    bits = [0]*8
    for i in range(8):
        bits[i]=1
        GPIO.output(dac,bits)
        time.sleep(0.01)
        if GPIO.input(comp) == 1:
            bits[i] = 0
    return bits
try:
    while(True):
        a = adc()
        value = b2d(a)
        v = value*3.3/256
        print(value,v)
        light = [0]*8
        n = int((value+1)//32)
        for i in range(n):
            light[7-i] = 1
        GPIO.output(leds, light)

finally:
    GPIO.output(dac, 0)

