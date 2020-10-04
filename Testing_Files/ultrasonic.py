import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

#variable declerations for ultrasonic
echo = 20
trig = 21
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.output(trig, False)
#let the thing sleep for 2 seconds
time.sleep(2)

print ("Measuring in Progress")

def measureDistanceCm():
    pulse_start = 0
    pulse_end = 0
    
    GPIO.output(trig, True)
    time.sleep(0.00001) #sleep for 1us to send trig signal
    GPIO.output(trig, False)
    
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    
    speed_of_sound = 34300 #speed of sound in cm/s
    
    distance = round(speed_of_sound*pulse_duration/2, 2) #divide time by 2 cause return time
    
    return distance

while True:
    distance = str(measureDistanceCm())
    print ("Distance: " + distance)
    time.sleep(0.5)