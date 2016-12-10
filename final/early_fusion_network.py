
import tensorflow as tf
import pdb
import numpy as np
from numpy import genfromtxt
import os

# Parameters
learning_rate = 0.001
training_iters = 1000000
batch_size = 30
display_step = 1

# Network Parameters
n_input_x = 10*60 # Input image x-dimension
n_input_y = 80 # Input image y-dimension
n_input_z = 3
n_classes = 12
n_predictions = 50

dropout = 0.75 # Dropout, probability to keep units

# tf Graph input
x = tf.placeholder(tf.float32, [None, n_input_x, n_input_y, n_input_z])
y = tf.placeholder(tf.float32, [None, n_classes], name="ground_truth")
keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)

def input_data():
    path = "/home/kendall/Documents/Development/CS463G/final/data/60x80/slow_fusion/"
    input_files = os.listdir(path + "input_data")
    ground_truth_files = os.listdir(path + "ground_truth")
    input_data = []
    ground_truth = []

    for i in range(len(input_files)):
    # for i in range(50):
        temp = np.genfromtxt(path + "input_data/" + input_files[i], delimiter=",")
        temp = temp.reshape((10, 60, 80, 3))
        input_data.append(temp)
        if i % 100 == 0:
            print "Importing input data: " + str(i) + " out of " + str(len(input_files))

    for i in range(len(ground_truth_files)):
    # for i in range(50):
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

training_data = input_data[0:input_data.shape[0]-n_predictions]
training_ground_truth = ground_truth[0:ground_truth.shape[0]-n_predictions]
prediction_data = input_data[input_data.shape[0]-n_predictions:input_data.shape[0]]
prediction_ground_truth = ground_truth[ground_truth.shape[0]-n_predictions:ground_truth.shape[0]]

def conv3d(x, W, b, strides=2, padding=0):
    # Conv2D wrapper, with bias and relu activation
    if padding == 0:
        x = tf.nn.conv3d(x, W, strides=[1, strides, strides, strides, 1], padding='SAME')
    else:
        x = tf.nn.conv3d(x, W, strides=[1, strides, strides, strides, 1], padding='VALID')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)

def cnn(x, weights, biases):

    frames = tf.reshape(x, [-1, 60, 80, 3, 10])

    # BEGIN CNN
    with tf.name_scope("conv1") as scope:
        conv1 = conv3d(frames, weights['wc1'], biases['bc1'], strides=2)
        conv1 = tf.reshape(conv1, [-1, 30, 40, 2 * 4])
        conv1 = tf.contrib.layers.batch_norm(conv1)
        conv1 = tf.reshape(conv1, [-1, 30, 40, 2, 4])

    with tf.name_scope("conv2") as scope:
        conv2 = conv3d(conv1, weights['wc2'], biases['bc2'], strides=2)
        conv2 = tf.reshape(conv2, [-1, 15, 20, 1 * 8])
        conv2 = tf.contrib.layers.batch_norm(conv2)
        conv2 = tf.reshape(conv2, [-1, 15, 20, 1, 8])

    with tf.name_scope("conv3") as scope:
        conv3 = conv3d(conv2, weights['wc3'], biases['bc3'], strides=2)
        conv3 = tf.reshape(conv3, [-1, 8, 10, 1 * 16])
        conv3 = tf.contrib.layers.batch_norm(conv3)
        conv3 = tf.reshape(conv3, [-1, 8, 10, 1, 16])

    with tf.name_scope("conv4") as scope:
        conv4 = conv3d(conv3, weights['wc4'], biases['bc4'], strides=2)
        conv4 = tf.reshape(conv4, [-1, 4, 5, 1 * 32])
        conv4 = tf.contrib.layers.batch_norm(conv4)
        conv4 = tf.reshape(conv4, [-1, 4, 5, 1, 32])

    with tf.name_scope("conv5") as scope:
        conv5 = conv3d(conv4, weights['wc5'], biases['bc5'], strides=2)
        conv5 = tf.reshape(conv5, [-1, 2, 3, 1 * 64])
        conv5 = tf.contrib.layers.batch_norm(conv5)
        conv5 = tf.reshape(conv5, [-1, 2, 3, 1, 64])

    conv_output = tf.reshape(b1234_conv5, [-1, 2*3*1*64])
    out = tf.add(tf.matmul(conv_output, weights['fc']), biases['fc'])
    out = tf.nn.dropout(out, dropout)

    return out

weights = {
    'wc1' : tf.get_variable("weights_1", shape=[3, 3, 1, 3, 4],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'wc2' : tf.get_variable("weights_5", shape=[3, 3, 1, 4, 8],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'wc3' : tf.get_variable("weights_9", shape=[3, 3, 1, 8, 16],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'wc4' : tf.get_variable("weights_15", shape=[3, 3, 1, 16, 32],
              initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'wc5' : tf.get_variable("weights_16", shape=[3, 3, 1, 32, 64],
              initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'fc' : tf.get_variable("weights_17", shape=[2*3*1*64, n_classes],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),
}

biases = {
    'bc1': tf.Variable(tf.zeros([4], dtype=tf.float32), name="biases_1", dtype=tf.float32),
    'bc2': tf.Variable(tf.zeros([8], dtype=tf.float32), name="biases_5", dtype=tf.float32),
    'bc3': tf.Variable(tf.zeros([16], dtype=tf.float32), name="biases_11", dtype=tf.float32),
    'bc4': tf.Variable(tf.zeros([32], dtype=tf.float32), name="biases_15", dtype=tf.float32),
    'bc5': tf.Variable(tf.zeros([64], dtype=tf.float32), name="biases_16", dtype=tf.float32),
    'fc': tf.Variable(tf.zeros([n_classes], dtype=tf.float32), name="biases_17", dtype=tf.float32),
}

pred = cnn(x, weights, biases)


# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Evaluate model
correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Initializing the variables
init = tf.initialize_all_variables()

# Launch the graph
with tf.Session() as sess:
    sess.run(init)
    overall_loss = []
    overall_acc = []
    prediction_acc = []
    prediction_acc_by_class = []

    for step in range(501):

        rand_batch = np.random.randint(training_data.shape[0]-batch_size)

        batch_x = input_data[rand_batch:rand_batch+batch_size].reshape((batch_size, n_input_x, n_input_y, n_input_z))
        batch_y = ground_truth[rand_batch:rand_batch+batch_size]

        sess.run(optimizer, feed_dict={x: batch_x, y: batch_y,
                                               keep_prob: dropout})

        loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x,
                                                                      y: batch_y,
                                                                      keep_prob: 1.})

        print "Step = " + str(step)
        print "Loss = " + str(np.mean(loss))
        print "Accuracy = " + str(np.mean(acc))

        overall_loss.append(np.mean(loss))
        overall_acc.append(np.mean(acc))

        if step % 10 == 0:
            acc_count = 0
            acc_by_class = np.zeros((12))
            for i in range(prediction_data.shape[0]):
                batch_x = prediction_data[i].reshape(1, n_input_x, n_input_y, n_input_z)
                batch_y = prediction_ground_truth[i]
                pred_val = sess.run(tf.nn.softmax(pred), feed_dict={x: batch_x})
                if np.argmax(pred_val) == np.argmax(prediction_ground_truth[i]):
                    acc_count = acc_count + 1
                    acc_by_class[np.argmax(pred_val)] = acc_by_class[np.argmax(pred_val)] + 1
            # pdb.set_trace()
            prediction_acc.append(float(float(acc_count) / prediction_data.shape[0]))
            prediction_acc_by_class.append(acc_by_class)

        step = step + 1

    overall_loss = np.array(overall_loss)
    overall_acc = np.array(overall_acc)
    np.savetxt("./overall_loss_early_fusion.csv", overall_loss, delimiter=",")
    np.savetxt("./overall_acc_early_fusion.csv", overall_acc, delimiter=",")

    prediction_acc = np.array(prediction_acc)
    np.savetxt("./pred_acc_early_fusion.csv", prediction_acc, delimiter=",")

    prediction_class_distribution = np.genfromtxt("./prediction_class_distribution.csv", delimiter=",")
    prediction_acc_by_class = np.array(prediction_acc_by_class)
    print "Prediction average by class = " + str(np.mean(prediction_acc_by_class, axis=0) / prediction_class_distribution)
    np.savetxt("./acc_by_class_early_fusion.csv", np.mean(prediction_acc_by_class, axis=0) / prediction_class_distribution, delimiter=",")
