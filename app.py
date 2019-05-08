import sys
import csv
import operator
import random
import math
import os.path


def loadDataset(trainingFile, testFile, trainingset=[], testset=[]):

    with open(trainingFile, "r") as trainingFile:
        lines = trainingFile.readlines();
        dataset = list(lines);

        for x in range(len(dataset)):
            trainingset.append(dataset[x].split())


    with open(testFile, "r") as testFile:
        lines = testFile.readlines()
        dataset = list(lines)
        for x in range(len(dataset)):
            testset.append(dataset[x].split())


def euclidean_distance(ins1, ins2, length):
    distance = 0;
    for x in range(length):
        distance += pow(float(ins1[x]) - float(ins2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1;
    for x in range(len(trainingSet)):
        dist = euclidean_distance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])

    return neighbors


def sortByClasses(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        dist = neighbors[x][-1]
        if dist in classVotes:
            classVotes[dist] += 1
        else:
            classVotes[dist] = 1

    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def getAccuracy(testset, predictions):
    correct = 0;
    for x in range(len(testset)):
        if testset[x][-1] == predictions[x]:
            correct += 1

    return (float(correct)/float(len(testset))) * 100.0

def main(trainingFile, testFile):
    trainingset = []
    testset = []
    loadDataset(trainingFile, testFile, trainingset, testset);
    results = []

    """
    iterate through each testinstance and find closesr neighbors based on euclidean distance and class votes. 
    """
    k = 1

    for x in range(len(testset)):
        neighbors = getNeighbors(trainingset, testset[x], k)
        result = sortByClasses(neighbors)
        results.append(result)
        print("predicted ="+repr(result)+'. actual='+repr(testset[x][-1]))

    accuracy = getAccuracy(testset, results)
    print('Accuracy: ' + repr(accuracy) + '%')


def isFile(fileName):
    if (not os.path.isfile(fileName)):
        raise ValueError("You must provide a valid filename as parameter")


if __name__ == "__main__":
    try:
        print("file name is ", sys.argv[2]);
        trainingFile = sys.argv[1]
        testFile = sys.argv[2]
        main(trainingFile, testFile)
        pass
    except Exception as e:
        print("You must provide a valid filename as parameter")
        raise