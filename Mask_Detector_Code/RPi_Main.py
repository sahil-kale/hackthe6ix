import RPi.GPIO as GPIO
from CV_API_Handler import *
import time
import cv2

# initial & global declerations
servo_pin = 19
servo_freq = 50
face_cascade = cv2.CascadeClassifier(
    '/home/pi/Downloads/haarcascade_frontalface_alt2.xml')
camera = cv2.VideoCapture(0)
currentServoDegree = 90


def GPIOinit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)


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


# takes in -100 to 100 percent of camera error from centre (-100 is left, 100 is right), Proportional constant
def setServoError(cameraError, kCameraP):
    degreeCorrectionAngle = cameraError * 0.9 * kCameraP
    setServoPosition(currentServoDegree-degreeCorrectionAngle)
    print(currentServoDegree)
    print(degreeCorrectionAngle)


def TakeScreenshot():
    image_name = 'Picture.jpg'
    cv2.imwrite(image_name, frame)
    HandleImageAPI()


def updateCamera():
    returnValue = -1
    scaleFactor = 0.4
    ret, Originalframe = camera.read()

    frame = cv2.resize(Originalframe, (0, 0), fx=scaleFactor, fy=scaleFactor)

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(grey, 1.1, 4)

    if len(faces) > 0:
        (x, y, w, z) = faces[0]
        faceX = int(x+w/2.0)
        faceY = int(y+z/2.0)
        #print(faceX, faceY)
        returnValue = faceX

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # else:
        #print("No faces detected")

    cv2.imshow('testFrame', frame)

    return int(returnValue)


# init stuff
GPIOinit()
servoPwm = GPIO.PWM(servo_pin, servo_freq)

servoPwm.start(7.5)

while True:
    xValue = updateCamera()
    print(xValue)

    if(xValue != -1):
        kServoCamConstant = 0.05
        kCameraMaxRange = 255
        kCameraMinRange = 0

        cameraError = (xValue-kCameraMinRange) / \
            (kCameraMaxRange-kCameraMinRange)*200-100
        setServoError(cameraError, kServoCamConstant)

        print(cameraError)

    key = cv2.waitKey(1)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()

GPIO.cleanup()
