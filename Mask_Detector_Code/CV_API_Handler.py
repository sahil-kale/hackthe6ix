# This program uses the Microsoft Azure Computer Vision Prediction API, it looks for an image created by ScreenshotHandler.py in the same directory and sends it over an API to get a prediction value

import urllib3
import json


def HandleImageAPI():
    # Open Image from Resources Folder
    with open('Picture.jpg', 'rb') as fp:
        binary_data = fp.read()

    # Create the required body JSON for the Azure API Body
    http = urllib3.PoolManager()

    # Make the HTTP Post Request
    r = http.request('POST', 'https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/bcd60e12-6248-434a-ad30-f25bec4b226c/classify/iterations/MaskModelV1/image', headers={
        'Prediction-Key': '57b3b8e01c5c4548bb73c245127a6354',
        'Content-Type': 'application/octet-stream',
    },
        body=binary_data
    )

    # Decode the JSON in a dictionary
    data = json.loads(r.data.decode('utf-8'))

    # Since the API returns the first predictions object as highest probability, we can use that to our advantage
    predicted_covering = data['predictions'][0]['tagName']
    predicted_probability = float(data['predictions'][0]['probability'])

    # Depending on the tag, print a response for fun
    if(str(predicted_covering) == 'Mask'):
        print('This person is wearing a mask! Probability: ' +
              str(round((predicted_probability*100), 2)) + '%')
        return
    else:
        print('This person is not wearing a mask! Shame on you! Probability: ' +
              str(round((predicted_probability*100), 2)) + '%')
        return
    # Print it out for debugging
