import RPi.GPIO as GPIO
GPIO.setwarnings(False)
from CV_API_Handler import *
from ultrasonic import *
from cardreader import *
from firebaselogger import *
import time
import cv2
import numpy as np


# All the dependencies

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate("/home/pi/Desktop/Code/Hackathon/myapp-7ce88-firebase-adminsdk-ttzn8-91a855cee4.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


# initial & global declerations
servo_pin = 19
servo_freq = 50
led_pin = 13
face_cascade = cv2.CascadeClassifier('/home/pi/Downloads/haarcascade_frontalface_alt2.xml')
face_cascade_bw = cv2.CascadeClassifier('/home/pi/Downloads/haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(0)
currentServoDegree = 90 # at the start, this number corrosponds to the inital ping.


def GPIOinit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setup(led_pin, GPIO.OUT)


def setServoPosition(degrees):
    lowEndMs = 1
    highEndMs = 2
    range = 180  # range in degrees
    periodMs = 1/servo_freq*1000
    global currentServoDegree

    dutyCycleForSelectedDegree = round(
        (degrees/range*(highEndMs-lowEndMs)+lowEndMs)/periodMs*100, 1)
    # print(dutyCycleForSelectedDegree)
    if(dutyCycleForSelectedDegree > highEndMs/periodMs * 100):
        print("High Bounds exceeded, sticking to bound")
        servoPwm.ChangeDutyCycle(highEndMs/periodMs * 100)
        currentServoDegree = range
    elif(dutyCycleForSelectedDegree < lowEndMs/periodMs * 100):
        print("Low Bounds exceeded, sticking to bound")
        servoPwm.ChangeDutyCycle(lowEndMs/periodMs * 100)
        currentServoDegree = 0
    else:
        servoPwm.ChangeDutyCycle(dutyCycleForSelectedDegree)
        currentServoDegree = degrees


# takes in -100 to 100 percent of camera
def setServoError(cameraError, kCameraP):
    degreeCorrectionAngle = cameraError * 0.9 * kCameraP
    setServoPosition(currentServoDegree-degreeCorrectionAngle)
    #print(currentServoDegree)
    #print(degreeCorrectionAngle)


# Set array for validation of centering of camera
stock_data = np.full(2, 100)


def TakeScreenshot():
    print('Taking Screenshot...')
    image_name = 'Picture.jpg'
    cv2.imwrite(image_name, Originalframe)
    HandleImageAPI()

# This function is used as a shift register to measure the last 20 measurements


def shiftRegister(shift_array, insertion_number):
    # Adds the number to the front of the list
    shift_array = np.insert(shift_array, 0, insertion_number)
    # Pops off the last number
    shift_array = np.delete(shift_array, -1)
    return shift_array

# This function checks whether all the values fall within a range, this range needs to be calibrated


def CenterCheck(array):
    # If any items are outside of range, it will set detected to true
    # Edit Lower And Upper Range Here
    lower_range = -100
    upper_range = 100

    # Every time this function is called, set this param to False
    NumOutOfRange = False

    for item in array:
        if item < lower_range or item > upper_range:
            NumOutOfRange = True

    # Checks to see if NumOutOfRange was set to True due to the outliar

    if NumOutOfRange:
        return False
    else:
        return True


def updateCamera(Originalframe):
    returnValue = -1 #default return value is -1 in case no face is found
    
    scaleFactor = 0.35
    

    frame = cv2.resize(Originalframe, (0, 0), fx=scaleFactor, fy=scaleFactor)

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    (thresh, black_and_white) = cv2.threshold(grey, 13, 22, cv2.THRESH_BINARY)
    
    #maskCentreX = -1
    #bw_threshold_min = 65
    #bw_threshold_max = 75
    #threshold2 = cv2.threshold(grey, bw_threshold_min, bw_threshold_max, cv2.THRESH_BINARY)[1]
    #contours = cv2.findContours(threshold2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours = contours[0] if len(contours) == 2 else contours[1]
    
    #for c in contours:
        #minContourLength = 90
        #minArea = 40
        #if(cv2.arcLength(c, True) > minContourLength and cv2.contourArea(c) > minArea):
            #cv2.drawContours(frame, [c], -1, (0,255,0),1)
            #d = max(contours, key = cv2.contourArea)
            #x,y,w,h = cv2.boundingRect(d)
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
            #maskCentreX = int(x+w/2.0)
            #print(maskCentreX)
    
    
    cv2.imshow('black_and_white', black_and_white)
    
    #create filters for different face types
    faces = face_cascade.detectMultiScale(grey, 1.1, 4)
    faces_bw = face_cascade_bw.detectMultiScale(black_and_white, 1.1, 4)  
    

    #these 2 types create bounding rectangles on the traces
    if len(faces) > 0:
        (x, y, w, z) = faces[0]
        faceX = int(x+w/2.0)
        faceY = int(y+z/2.0)
        #print(faceX, faceY)
        returnValue = faceX

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
    if len(faces_bw) > 0:
        (x, y, w, z) = faces_bw[0]
        faceX2 = int(x+w/2.0)
        for (x, y, w, h) in faces_bw:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        returnValue = faceX2

    cv2.imshow('testFrame', frame)

    return int(returnValue)


def logEmployeeInteraction(led_pin):
    GPIO.output(led_pin, True)
    scannedCard = str(readCard())
    print(scannedCard)
    LogTime(scannedCard.strip(), db)
    GPIO.output(led_pin, False)
    time.sleep(0.3)
    GPIO.output(led_pin, True)
    time.sleep(1.5)
    GPIO.output(led_pin, False)
    

# init stuff
GPIOinit()
servoPwm = GPIO.PWM(servo_pin, servo_freq)
#GPIO.output(led_pin, False)

#servoPwm.start(7.5)

while True:
    GPIO.output(led_pin, True)
    arrestServoMovement = False
    ret, Originalframe = camera.read()
    xValue = updateCamera(Originalframe) #calls the update camera function
    #print(xValue)
    measuredDistance = measureDistanceCm()
    print(measuredDistance)
    triggerDistance = 69

    if(xValue != -1 and measuredDistance < triggerDistance): #needs to meet these conditions to actually move the servo
        kServoCamConstant = 0.000
        kCameraMaxRange = 255
        kCameraMinRange = 0

        cameraError = (xValue-kCameraMinRange)/(kCameraMaxRange-kCameraMinRange)*200-100
        #if(not arrestServoMovement):
            #setServoError(cameraError, kServoCamConstant)

        stock_data = shiftRegister(stock_data, cameraError)

        # Check to see if the last 20 values are consistent
        if(CenterCheck(stock_data)):
            stock_data = np.full(2, 100)
            TakeScreenshot()
            arrestServoMovement = True
            print("Please scan your card")
            logEmployeeInteraction(led_pin)
            
        

    key = cv2.waitKey(1)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()

GPIO.cleanup()