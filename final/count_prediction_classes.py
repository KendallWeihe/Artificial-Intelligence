import numpy as np
import pdb
import os


def input_data():
    path = "/home/kendall/Documents/Development/CS463G/final/data/60x80/late_fusion/"
    input_files = os.listdir(path + "input_data")
    ground_truth_files = os.listdir(path + "ground_truth")
    input_data = []
    ground_truth = []

    for i in range(len(input_files)):
    # for i in range(100):
        temp = np.genfromtxt(path + "input_data/" + input_files[i], delimiter=",")
        temp = temp.reshape((2, 60, 80, 3))
        input_data.append(temp)
        if i % 100 == 0:
            print "Importing input data: " + str(i) + " out of " + str(len(input_files))

    for i in range(len(ground_truth_files)):
    # for i in range(100):
        temp = np.genfromtxt(path + "ground_truth/" + ground_truth_files[i], delimiter=",")
        ground_truth.append(temp)
        if i % 100 == 0:
            print "Importing ground truth: " + str(i) + " out of " + str(len(ground_truth_files))

    return np.array(input_data), np.array(ground_truth)

input_data, ground_truth = input_data()

randomize_order = np.genfromtxt("./random_order.csv", delimiter=",")
randomize_order = np.array(randomize_order, dtype=np.int)
input_data = input_data[randomize_order]
ground_truth = ground_truth[randomize_order]

n_predictions = 50
training_data = input_data[0:input_data.shape[0]-n_predictions]
training_ground_truth = ground_truth[0:ground_truth.shape[0]-n_predictions]
prediction_data = input_data[input_data.shape[0]-n_predictions:input_data.shape[0]]
prediction_ground_truth = ground_truth[ground_truth.shape[0]-n_predictions:ground_truth.shape[0]]


count_list = np.zeros((12))
for i in range(prediction_ground_truth.shape[0]):
    count_list[np.argmax(prediction_ground_truth[i])] = count_list[np.argmax(prediction_ground_truth[i])] + 1

print count_list
np.savetxt("./prediction_class_distribution.csv", count_list, delimiter=",")
