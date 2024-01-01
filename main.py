from machine import ADC, Pin, PWM, Timer
import math 
import utime

maxVal=180

class Servo:
    def __init__(self, pin: int or Pin or PWM, minVal=1000, maxVal=6500):
        if isinstance(pin, int):
            pin = Pin(pin, Pin.OUT)
        if isinstance(pin, Pin):
            self.__pwm = PWM(pin)
        if isinstance(pin, PWM):
            self.__pwm = pin
        self.__pwm.freq(50)
        self.minVal = minVal
        self.maxVal = maxVal
 
    def deinit(self):
        self.__pwm.deinit()
 
    def sMap(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def goto(self, angle: int):
        value=round(self.sMap(max(0,min(180,angle)),0,180,0,maxVal))
        delta = self.maxVal-self.minVal
        target = int(self.minVal + ((max(0,min(maxVal,value)) / maxVal) * delta))
        self.__pwm.duty_u16(target) #/65025
 
    def free(self):
        self.__pwm.duty_u16(0)

def on_timer(timer):
    relay.toggle()


servo = Servo(0)#GP0  
led = Pin("LED", Pin.OUT)#GP25
relay = Pin("GP26", Pin.OUT)#GP26
relay.toggle()
  
i=0
startangle=45
endangle=startangle-55
rotatedelay=0.3
ontime=1300 #ms


timer = Timer(-1) #virtual timer only supported (-1)
timer.init(mode=Timer.ONE_SHOT, period=ontime, callback=on_timer)


servo.goto(startangle)
utime.sleep(rotatedelay)
led.toggle() 
servo.goto(endangle)
utime.sleep(rotatedelay)
led.toggle() 
servo.goto(startangle)
utime.sleep(rotatedelay)
led.toggle()
servo.free()
#while True:
#    i=(i+10)%360
#    servo.goto(90+20*math.sin(i/360*2*math.pi))
#    utime.sleep(0.2)
#    led.toggle() 
    
    
        
    







