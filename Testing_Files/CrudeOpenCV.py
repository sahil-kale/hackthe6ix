import cv2

camera = cv2.VideoCapture(0)

imageCounter = 0

while True:
    ret, frame = camera.read()
    cv2.imshow("TestFrame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()