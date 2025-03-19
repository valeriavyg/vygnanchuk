import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt 

GPIO.setmode(GPIO.BCM)

dac = [8,11,7,1,0,5,12,6]
leds = [2,3,4,17,27,22,10,9]
comp = 14
troyka = 13

GPIO.setup(dac,GPIO.OUT)
GPIO.setup(leds,GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT)

t = 0

def volts():
    print(adc())
    return(GPIO.input(troyka))

def binary(a):
    return[int(n) for n in bin(a)[2:].zfill(8)]

def led():
    GPIO.output(leds, binary(volts()))

def adc():
    n = [0]*8
    for i in range(8):
        n[i] = 1
        GPIO.output(dac,n)
        time.sleep(0.01)
        if GPIO.input(comp)==1:
            n[i] = 0
    return int (''.join(map(str,n)),2)


t0 = time.time()

try:
    n = []
    GPIO.output(troyka, 1)
    while adc() < 207:
        volts()
        n.append(adc())
        t+= 0.01
    GPIO.output(troyka, 0)
    while adc() > 10:
        volts()
        n.append(adc())
        t+= 0.01

    strn = [str(item) for item in n]
    stra = [str(item) for item in [1000, 0.013]]

    t1 = time.time()
    t = t1-t0
    print(t)
    print(t/len(n))
    print(len(n)/t)
    rate = len(n)/t if t>0 else 0
    step = 3.3/255
    with open("data1.txt", "w") as f:
        for value in n:
            f.write(str(value)+ "\n")
    with open("settings1.txt", "w") as f:
        f.write(f"частота:{rate:.2f}Гц")
        f.write(f"шаг квантования:{step:.2f}Гц")

finally:
    GPIO.output(dac,0)
    GPIO.output(troyka,0)
    GPIO.cleanup(dac) 
plt.plot(n)
plt.show()
