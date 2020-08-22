#This program handles the screenshot taking and will run locally on a Raspberry Pi connected to the internet. It will take an image and send it over CV_API_Handler.py which connects to Microsoft Azure Services

import cv2
from CV_API_Handler import *

# Create camera object linked to Video Capture
camera = cv2.VideoCapture(0)

# Create running loop while the program is executing

while True:
    # Create ret and frame
    ret, frame = camera.read()

    # Show frame
    cv2.imshow("Unmasked Video Capture Frame", frame)

    # Look for the keys to determine whether to take a screenshot or to exit the while loop
    key = cv2.waitKey(1)

    if (key == 32):
        # Take a screenshot named Screenshot
        image_name = 'Picture.jpg'
        cv2.imwrite(image_name, frame)
        HandleImageAPI()

    if (key == 27):
        break

# Stop Camera once Escape is hit
camera.release()

# Removes the window showing the live feed
cv2.destroyAllWindows()
