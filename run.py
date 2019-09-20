#!/usr/bin/env python3

from imageai.Prediction import ImagePrediction
import os

execution_path = os.getcwd()

prediction = ImagePrediction()
prediction.setModelTypeAsDenseNet()
prediction.setModelPath(os.path.join(execution_path, "trained_data/DenseNet-BC-121-32.h5"))
prediction.loadModel()

for x in range(5):
    predictions, probabilities = prediction.predictImage(os.path.join(execution_path, "test_images/%d.JPG" % (x+1)), result_count=5 )
    for eachPrediction, eachProbability in zip(predictions, probabilities):
        print(eachPrediction , " : " , eachProbability)