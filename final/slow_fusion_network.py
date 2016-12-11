
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

    frames = tf.split(1, 10, x)
    batch_1 = tf.reshape(tf.pack([frames[0], frames[1], frames[2], frames[3]]), [-1, 60, 80, 3, 4])
    batch_2 = tf.reshape(tf.pack([frames[2], frames[3], frames[4], frames[5]]), [-1, 60, 80, 3, 4])
    batch_3 = tf.reshape(tf.pack([frames[4], frames[5], frames[6], frames[7]]), [-1, 60, 80, 3, 4])
    batch_4 = tf.reshape(tf.pack([frames[6], frames[7], frames[8], frames[9]]), [-1, 60, 80, 3, 4])

    # BEGIN BATCH 1 LAYER 1
    with tf.name_scope("batch_1_layer_1") as scope:
        b1_conv1 = conv3d(batch_1, weights['b1_wc1'], biases['b1_bc1'], strides=2)
        b1_conv1 = tf.reshape(b1_conv1, [-1, 30, 40, 2 * 4])
        b1_conv1 = tf.contrib.layers.batch_norm(b1_conv1)
        b1_conv1 = tf.reshape(b1_conv1, [-1, 30, 40, 2, 4])

    with tf.name_scope("batch_1_layer_2") as scope:
        b1_conv2 = conv3d(b1_conv1, weights['b1_wc2'], biases['b1_bc2'], strides=2)
        b1_conv2 = tf.reshape(b1_conv2, [-1, 15, 20, 1 * 8])
        b1_conv2 = tf.contrib.layers.batch_norm(b1_conv2)
        b1_conv2 = tf.reshape(b1_conv2, [-1, 15, 20, 1, 8])

    # BEGIN BATCH 2 LAYER 1
    with tf.name_scope("batch_2_layer_1") as scope:
        b2_conv1 = conv3d(batch_2, weights['b2_wc1'], biases['b2_bc1'], strides=2)
        b2_conv1 = tf.reshape(b2_conv1, [-1, 30, 40, 2 * 4])
        b2_conv1 = tf.contrib.layers.batch_norm(b2_conv1)
        b2_conv1 = tf.reshape(b2_conv1, [-1, 30, 40, 2, 4])

    with tf.name_scope("batch_2_layer_2") as scope:
        b2_conv2 = conv3d(b2_conv1, weights['b2_wc2'], biases['b2_bc2'], strides=2)
        b2_conv2 = tf.reshape(b2_conv2, [-1, 15, 20, 1 * 8])
        b2_conv2 = tf.contrib.layers.batch_norm(b2_conv2)
        b2_conv2 = tf.reshape(b2_conv2, [-1, 15, 20, 1, 8])

    # BEGIN BATCH 3 LAYER 1
    with tf.name_scope("batch_3_layer_1") as scope:
        b3_conv1 = conv3d(batch_3, weights['b3_wc1'], biases['b3_bc1'], strides=2)
        b3_conv1 = tf.reshape(b3_conv1, [-1, 30, 40, 2 * 4])
        b3_conv1 = tf.contrib.layers.batch_norm(b3_conv1)
        b3_conv1 = tf.reshape(b3_conv1, [-1, 30, 40, 2, 4])

    with tf.name_scope("batch_3_layer_2") as scope:
        b3_conv2 = conv3d(b3_conv1, weights['b3_wc2'], biases['b3_bc2'], strides=2)
        b3_conv2 = tf.reshape(b3_conv2, [-1, 15, 20, 1 * 8])
        b3_conv2 = tf.contrib.layers.batch_norm(b3_conv2)
        b3_conv2 = tf.reshape(b3_conv2, [-1, 15, 20, 1, 8])

    # BEGIN BATCH 4 LAYER 1
    with tf.name_scope("batch_4_layer_1") as scope:
        b4_conv1 = conv3d(batch_4, weights['b4_wc1'], biases['b4_bc1'], strides=2)
        b4_conv1 = tf.reshape(b4_conv1, [-1, 30, 40, 2 * 4])
        b4_conv1 = tf.contrib.layers.batch_norm(b4_conv1)
        b4_conv1 = tf.reshape(b4_conv1, [-1, 30, 40, 2, 4])

    with tf.name_scope("batch_4_layer_2") as scope:
        b4_conv2 = conv3d(b4_conv1, weights['b4_wc2'], biases['b4_bc2'], strides=2)
        b4_conv2 = tf.reshape(b4_conv2, [-1, 15, 20, 1 * 8])
        b4_conv2 = tf.contrib.layers.batch_norm(b4_conv2)
        b4_conv2 = tf.reshape(b4_conv2, [-1, 15, 20, 1, 8])

    batch_12 = tf.concat(1, (b1_conv2, b2_conv2))
    batch_34 = tf.concat(1, (b3_conv2, b4_conv2))

    # BEGIN BATCHES 1 & 2 LAYERS 3 & 4
    with tf.name_scope("batch_12_layer_3") as scope:
        b12_conv3 = conv3d(batch_12, weights['b12_wc3'], biases['b12_bc3'], strides=2)
        b12_conv3 = tf.reshape(b12_conv3, [-1, 15, 10, 1 * 16])
        b12_conv3 = tf.contrib.layers.batch_norm(b12_conv3)
        b12_conv3 = tf.reshape(b12_conv3, [-1, 15, 10, 1, 16])

    with tf.name_scope("batch_12_layer_4") as scope:
        b12_conv4 = conv3d(b12_conv3, weights['b12_wc4'], biases['b12_bc4'], strides=2)
        b12_conv4 = tf.reshape(b12_conv4, [-1, 8, 5, 1 * 32])
        b12_conv4 = tf.contrib.layers.batch_norm(b12_conv4)
        b12_conv4 = tf.reshape(b12_conv4, [-1, 8, 5, 1, 32])

    # BEGIN BATCHES 3 & 4 LAYERS 3 & 4
    with tf.name_scope("batch_34_layer_3") as scope:
        b34_conv3 = conv3d(batch_34, weights['b34_wc3'], biases['b34_bc3'], strides=2)
        b34_conv3 = tf.reshape(b34_conv3, [-1, 15, 10, 1 * 16])
        b34_conv3 = tf.contrib.layers.batch_norm(b34_conv3)
        b34_conv3 = tf.reshape(b34_conv3, [-1, 15, 10, 1, 16])

    with tf.name_scope("batch_34_layer_4") as scope:
        b34_conv4 = conv3d(b34_conv3, weights['b34_wc4'], biases['b34_bc4'], strides=2)
        b34_conv4 = tf.reshape(b34_conv4, [-1, 8, 5, 1 * 32])
        b34_conv4 = tf.contrib.layers.batch_norm(b34_conv4)
        b34_conv4 = tf.reshape(b34_conv4, [-1, 8, 5, 1, 32])

    batch_1234 = tf.concat(1, (b12_conv4, b34_conv4))

    # PASS THE LAST BATCH THROUGH THE FINAL LAYER
    with tf.name_scope("batch_1234_layer_5") as scope:
        b1234_conv5 = conv3d(batch_1234, weights['b1234_wc5'], biases['b1234_bc5'], strides=2)
        b1234_conv5 = tf.reshape(b1234_conv5, [-1, 8, 3, 1 * 64])
        b1234_conv5 = tf.contrib.layers.batch_norm(b1234_conv5)
        b1234_conv5 = tf.reshape(b1234_conv5, [-1, 8, 3, 1, 64])

    conv_output = tf.reshape(b1234_conv5, [-1, 8*3*1*64])
    out = tf.add(tf.matmul(conv_output, weights['fc']), biases['fc'])
    out = tf.nn.dropout(out, dropout)

    return out

weights = {
    'b1_wc1' : tf.get_variable("weights_1", shape=[3, 3, 1, 4, 4],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b2_wc1' : tf.get_variable("weights_2", shape=[3, 3, 1, 4, 4],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b3_wc1' : tf.get_variable("weights_3", shape=[3, 3, 1, 4, 4],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b4_wc1' : tf.get_variable("weights_4", shape=[3, 3, 1, 4, 4],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b1_wc2' : tf.get_variable("weights_5", shape=[3, 3, 1, 4, 8],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b2_wc2' : tf.get_variable("weights_6", shape=[3, 3, 1, 4, 8],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b3_wc2' : tf.get_variable("weights_7", shape=[3, 3, 1, 4, 8],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b4_wc2' : tf.get_variable("weights_8", shape=[3, 3, 1, 4, 8],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b12_wc3' : tf.get_variable("weights_9", shape=[3, 3, 1, 8, 16],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b34_wc3' : tf.get_variable("weights_11", shape=[3, 3, 1, 8, 16],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b12_wc4' : tf.get_variable("weights_13", shape=[3, 3, 1, 16, 32],
              initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b34_wc4' : tf.get_variable("weights_15", shape=[3, 3, 1, 16, 32],
              initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'b1234_wc5' : tf.get_variable("weights_16", shape=[3, 3, 1, 32, 64],
              initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),

    'fc' : tf.get_variable("weights_17", shape=[8*3*1*64, n_classes],
               initializer=tf.contrib.layers.xavier_initializer(), dtype=tf.float32),
}

biases = {
    'b1_bc1': tf.Variable(tf.zeros([4], dtype=tf.float32), name="biases_1", dtype=tf.float32),
    'b2_bc1': tf.Variable(tf.zeros([4], dtype=tf.float32), name="biases_2", dtype=tf.float32),
    'b3_bc1': tf.Variable(tf.zeros([4], dtype=tf.float32), name="biases_3", dtype=tf.float32),
    'b4_bc1': tf.Variable(tf.zeros([4], dtype=tf.float32), name="biases_4", dtype=tf.float32),
    'b1_bc2': tf.Variable(tf.zeros([8], dtype=tf.float32), name="biases_5", dtype=tf.float32),
    'b2_bc2': tf.Variable(tf.zeros([8], dtype=tf.float32), name="biases_6", dtype=tf.float32),
    'b3_bc2': tf.Variable(tf.zeros([8], dtype=tf.float32), name="biases_7", dtype=tf.float32),
    'b4_bc2': tf.Variable(tf.zeros([8], dtype=tf.float32), name="biases_8", dtype=tf.float32),
    'b12_bc3': tf.Variable(tf.zeros([16], dtype=tf.float32), name="biases_9", dtype=tf.float32),
    'b34_bc3': tf.Variable(tf.zeros([16], dtype=tf.float32), name="biases_11", dtype=tf.float32),
    'b12_bc4': tf.Variable(tf.zeros([32], dtype=tf.float32), name="biases_13", dtype=tf.float32),
    'b34_bc4': tf.Variable(tf.zeros([32], dtype=tf.float32), name="biases_15", dtype=tf.float32),
    'b1234_bc5': tf.Variable(tf.zeros([64], dtype=tf.float32), name="biases_16", dtype=tf.float32),
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
    np.savetxt("./overall_loss_slow_fusion.csv", overall_loss, delimiter=",")
    np.savetxt("./overall_acc_slow_fusion.csv", overall_acc, delimiter=",")

    prediction_acc = np.array(prediction_acc)
    np.savetxt("./pred_acc_slow_fusion.csv", prediction_acc, delimiter=",")

    prediction_class_distribution = np.genfromtxt("./prediction_class_distribution.csv", delimiter=",")
    prediction_acc_by_class = np.array(prediction_acc_by_class)
    print "Prediction average by class = " + str(np.mean(prediction_acc_by_class, axis=0) / prediction_class_distribution)
    np.savetxt("./mean_acc_by_class_slow_fusion.csv", np.mean(prediction_acc_by_class, axis=0) / prediction_class_distribution, delimiter=",")
    np.savetxt("./acc_by_class_slow_fusion.csv", prediction_acc_by_class, delimiter=",")
