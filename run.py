#!/usr/bin/env python3

import os
import time
from imageai.Prediction import ImagePrediction
from adafruit_servokit import ServoKit
from picamera import PiCamera
from gpiozero import MotionSensor

# Image AI Setup
execution_path = os.getcwd()
prediction = ImagePrediction()
prediction.setModelTypeAsDenseNet()
prediction.setModelPath(os.path.join(execution_path, "trained_data/DenseNet-BC-121-32.h5"))
print('Loading model...')
prediction.loadModel()

# Config
authorizedUsers = {
    "goose": 0, 
    "hen": 0, 
    "cock": 0, 
    "ostrich": 5, 
    "vulture": 5
}
timeBetweenCheck = 10

# Servo
kit = ServoKit(channels=16)
servo = kit.servo[1]

# Camera
camera = PiCamera()
imagePath = 'ducks.jpg'

# Motion sensor
pir = MotionSensor(4)

# Functions
def openFood(): 
    servo.angle = 180

def closeFood(): 
    servo.angle = 0

def imageHasAuthorizedUser(imagePath):
    predictions, probabilities = prediction.predictImage(os.path.join(execution_path, imagePath), result_count=5)
    for thePrediction, probability in zip(predictions, probabilities):
        print("%s - %s" % (thePrediction, probability))

    for thePrediction, probability in zip(predictions, probabilities):


        if thePrediction in authorizedUsers.keys() and authorizedUsers[thePrediction] <= float(probability):
            return True

    return False

print('Begining sentry')

# Main run loop:
while True:
    pir.wait_for_motion()
    print("Motion detected!")

    print("Taking picture, identifying ducks")
    # camera.start_preview()
    # camera.capture(imagePath)
    # camera.stop_preview()

    # TODO: Use motion detection sensor to not close food if any motion, not just re-detection
    if imageHasAuthorizedUser(imagePath): 
        print("Duck detected, opening food")
        openFood()
    else:
        print("No duck detected, closing food")
        closeFood()

    time.sleep(timeBetweenCheck)