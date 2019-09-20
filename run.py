#!/usr/bin/env python3

import os
import time
from imageai.Prediction import ImagePrediction
from adafruit_servokit import ServoKit
from picamera import PiCamera

# Image AI Setup
execution_path = os.getcwd()
prediction = ImagePrediction()
prediction.setModelTypeAsDenseNet()
prediction.setModelPath(os.path.join(execution_path, "trained_data/DenseNet-BC-121-32.h5"))
prediction.loadModel()

# Config
authorizedUsers = {
    "goose": 0, 
    "hen": 0, 
    "cock": 0, 
    "ostrich": 5, 
    "vulture": 5
}
timeBetweenCheck = 30

# Servo
kit = ServoKit(channels=16)
servo = kit.servo[1]

# Camera
camera = PiCamera()
imagePath = 'ducks.jpg'

# Functions
def openFood(): 
    servo.angle = 180

def openFood(): 
    servo.angle = 0

def imageHasAuthorizedUser(imagePath):
    predictions, probabilities = prediction.predictImage(os.path.join(execution_path, imagePath), result_count=5)
    for prediction, probability in zip(predictions, probabilities):
        if authorizedUsers[prediction] <= probability:
            return True

    return False

# Main run loop:
while True:
    print("Taking picture, identifying ducks")
    camera.startPreview()
    camera.capture(imagePath)
    camera.stopPreview()

    # TODO: Use motion detection sensor to not close food if any motion, not just re-detection
    if imageHasAuthorizedUser(imagePath): 
        print("Duck detected, opening food")
        openFood()
    else:
        print("No duck detected, closing food")
        closeFood()

    time.sleep(timeBetweenCheck)