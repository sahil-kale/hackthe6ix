import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

servo_pin = 19
servo_freq = 50
GPIO.setup(servo_pin, GPIO.OUT)

servoPwm = GPIO.PWM(servo_pin, servo_freq)
servoPwm.start(7.5);

def setServoPositionDegrees(degrees): #function, degrees from 0-180
    
    lowEndMs = 1
    highEndMs = 2
    range = 180 #range in degrees
    periodMs = 1/servo_freq*1000
    
    dutyCycleForSelectedDegree = round((degrees/range*(highEndMs-lowEndMs)+lowEndMs)/periodMs*100, 1)
    servoPwm.ChangeDutyCycle(dutyCycleForSelectedDegree)
    print(dutyCycleForSelectedDegree)
    
    

while True:    
    iterationNumber = 0
    setServoPositionDegrees(iterationNumber)
    if(iterationNumber == 180):
        iterationNumber = 0
    
    iterationNumber += 1
    time.sleep(0.01)
    print (iterationNumber)