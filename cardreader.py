import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def writeToCard(text):
    reader.write(text)
    print("Text Successfully Written")
    
def readCard():
    id, text = reader.read()
    return text