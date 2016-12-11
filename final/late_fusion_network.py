
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
n_input_x = 2*60 # Input image x-dimension
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

    early = tf.reshape(tf.split(1, 2, x)[0], [-1, 60, 80, 3, 1])
    late = tf.reshape(tf.split(1, 2, x)[1], [-1, 60, 80, 3, 1])

    # BEGIN EARLY NETWORK -------------------------------------------------------
    with tf.name_scope("early_conv1") as scope:
        early_conv1 = conv3d(early, weights['ewc1'], biases['ebc1'], strides=2)
        early_conv1 = tf.reshape(early_conv1, [-1, 30, 40, 2 * 4])
        early_conv1 = tf.contrib.layers.batch_norm(early_conv1)
        early_conv1 = tf.reshape(early_conv1, [-1, 30, 40, 2, 4])

    with tf.name_scope("early_conv2") as scope:
        early_conv2 = conv3d(early_conv1, weights['ewc2'], biases['ebc2'], strides=2)
        early_conv2 = tf.reshape(early_conv2, [-1, 15, 20, 1 * 8])
        early_conv2 = tf.contrib.layers.batch_norm(early_conv2)
        early_conv2 = tf.reshape(early_conv2, [-1, 15, 20, 1, 8])
        # conv2 = maxpool3d(conv2, k=2)

    with tf.name_scope("early_conv3") as scope:
        early_conv3 = conv3d(early_conv2, weights['ewc3'], biases['ebc3'], strides=2)
        early_conv3 = tf.reshape(early_conv3, [-1, 8, 10, 1 * 16])
        early_conv3 = tf.contrib.layers.batch_norm(early_conv3)
        early_conv3 = tf.reshape(early_conv3, [-1, 8, 10, 1, 16])

    with tf.name_scope("early_conv4") as scope:
        early_conv4 = conv3d(early_conv3, weights['ewc4'], biases['ebc4'], strides=2)
        early_conv4 = tf.reshape(early_conv4, [-1, 4, 5, 1 * 32])
        early_conv4 = tf.contrib.layers.batch_norm(early_conv4)
        early_conv4 = tf.reshape(early_conv4, [-1, 4, 5, 1, 32])

    with tf.name_scope("early_conv5") as scope:
        early_conv5 = conv3d(early_conv4, weights['ewc5'], biases['ebc5'], strides=2)
        early_conv5 = tf.reshape(early_conv5, [-1, 2, 3, 1 * 64])
        early_conv5 = tf.contrib.layers.batch_norm(early_conv5)
        early_conv5 = tf.reshape(early_conv5, [-1, 2 * 3 * 1 * 64])

    # BEGIN LATE NETWORK -------------------------------------------------------
    with tf.name_scope("late_conv1") as scope:
        late_conv1 = conv3d(late, weights['lwc1'], biases['lbc1'], strides=2)
        late_conv1 = tf.reshape(late_conv1, [-1, 30, 40, 2 * 4])
        late_conv1 = tf.contrib.layers.batch_norm(late_conv1)
        late_conv1 = tf.reshape(late_conv1, [-1, 30, 40, 2, 4])

    with tf.name_scope("late_conv2") as scope:
        late_conv2 = conv3d(late_conv1, weights['lwc2'], biases['lbc2'], strides=2)
        late_conv2 = tf.reshape(late_conv2, [-1, 15, 20, 1 * 8])
        late_conv2 = tf.contrib.layers.batch_norm(late_conv2)
        late_conv2 = tf.reshape(late_conv2, [-1, 15, 20, 1, 8])
        # conv2 = maxpool3d(conv2, k=2)

    with tf.name_scope("late_conv3") as scope:
        late_conv3 = conv3d(late_conv2, weights['lwc3'], biases['lbc3'], strides=2)
        late_conv3 = tf.reshape(late_conv3, [-1, 8, 10, 1 * 16])
        late_conv3 = tf.contrib.layers.batch_norm(late_conv3)
        late_conv3 = tf.reshape(late_conv3, [-1, 8, 10, 1, 16])

    with tf.name_scope("late_conv4") as scope:
        late_conv4 = conv3d(late_conv3, weights['lwc4'], biases['lbc4'], strides=2)
        late_conv4 = tf.reshape(late_conv4, [-1, 4, 5, 1 * 32])
        late_conv4 = tf.contrib.layers.batch_norm(late_conv4)
        late_conv4 = tf.reshape(late_conv4, [-1, 4, 5, 1, 32])

    with tf.name_scope("late_conv5") as scope:
        late_conv5 = conv3d(late_conv4, weights['lwc5'], biases['lbc5'], strides=2)
        late_conv5 = tf.reshape(late_conv5, [-1, 2, 3, 1 * 64])
        late_conv5 = tf.contrib.layers.batch_norm(late_conv5)
        late_conv5 = tf.reshape(late_conv5, [-1, 2 * 3 * 1 * 64])

    fusion_concat = tf.concat(1, (early_conv5, late_conv5))
    out = tf.add(tf.matmul(fusion_concat, weights['fc']), biases['fc'])
    out = tf.nn.dropout(out, dropout)

    return out

weights = {
    'ewc1' : tf.get_variable("weights_1", shape=[3, 3, 1, 1, 4],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'ewc2' : tf.get_variable("weights_2", shape=[3, 3, 1, 4, 8],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'ewc3' : tf.get_variable("weights_3", shape=[3, 3, 1, 8, 16],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'ewc4' : tf.get_variable("weights_4", shape=[3, 3, 1, 16, 32],
              initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'ewc5' : tf.get_variable("weights_5", shape=[3, 3, 1, 32, 64],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'lwc1' : tf.get_variable("weights_6", shape=[3, 3, 1, 1, 4],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'lwc2' : tf.get_variable("weights_7", shape=[3, 3, 1, 4, 8],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'lwc3' : tf.get_variable("weights_8", shape=[3, 3, 1, 8, 16],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'lwc4' : tf.get_variable("weights_9", shape=[3, 3, 1, 16, 32],
              initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'lwc5' : tf.get_variable("weights_10", shape=[3, 3, 1, 32, 64],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'fc' : tf.get_variable("weights_11", shape=[2*3*1*64*2, n_classes],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),
}

biases = {
    'ebc1': tf.Variable(tf.zeros([4], dtype=tf.float32), name="biases_1", dtype=tf.float32),
    'ebc2': tf.Variable(tf.zeros([8], dtype=tf.float32), name="biases_2", dtype=tf.float32),
    'ebc3': tf.Variable(tf.zeros([16], dtype=tf.float32), name="biases_3", dtype=tf.float32),
    'ebc4': tf.Variable(tf.zeros([32], dtype=tf.float32), name="biases_4", dtype=tf.float32),
    'ebc5': tf.Variable(tf.zeros([64], dtype=tf.float32), name="biases_5", dtype=tf.float32),
    'lbc1': tf.Variable(tf.zeros([4], dtype=tf.float32), name="biases_6", dtype=tf.float32),
    'lbc2': tf.Variable(tf.zeros([8], dtype=tf.float32), name="biases_7", dtype=tf.float32),
    'lbc3': tf.Variable(tf.zeros([16], dtype=tf.float32), name="biases_8", dtype=tf.float32),
    'lbc4': tf.Variable(tf.zeros([32], dtype=tf.float32), name="biases_9", dtype=tf.float32),
    'lbc5': tf.Variable(tf.zeros([64], dtype=tf.float32), name="biases_10", dtype=tf.float32),
    'fc': tf.Variable(tf.zeros([n_classes], dtype=tf.float32), name="biases_11", dtype=tf.float32),
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
    np.savetxt("./overall_loss_late_fusion.csv", overall_loss, delimiter=",")
    np.savetxt("./overall_acc_late_fusion.csv", overall_acc, delimiter=",")

    prediction_acc = np.array(prediction_acc)
    np.savetxt("./pred_acc_late_fusion.csv", prediction_acc, delimiter=",")

    prediction_class_distribution = np.genfromtxt("./prediction_class_distribution.csv", delimiter=",")
    prediction_acc_by_class = np.array(prediction_acc_by_class)
    print "Prediction average by class = " + str(np.mean(prediction_acc_by_class, axis=0) / prediction_class_distribution)
    np.savetxt("./mean_acc_by_class_late_fusion.csv", np.mean(prediction_acc_by_class, axis=0) / prediction_class_distribution, delimiter=",")
    np.savetxt("./acc_by_class_late_fusion.csv", prediction_acc_by_class, delimiter=",")
