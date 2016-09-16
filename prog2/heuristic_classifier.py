import numpy as np
import tensorflow as tf
import pdb

'''
A Multilayer Perceptron implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

# Parameters
learning_rate = 0.001
training_epochs = 4100
batch_size = 7
display_step = 500

# Network Parameters
n_hidden_1 = 256 # 1st layer number of features
n_hidden_2 = 256 # 2nd layer number of features
n_input = 6 * 12 # MNIST data input (img shape: 28*28)
n_classes = 7 # MNIST total classes (0-9 digits)

# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])

# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.sigmoid(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.sigmoid(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.initialize_all_variables()

def input_data():
    puzzle_states = []
    classes = []
    for i in range(1536):
        filename = "collect_data/ground_truth/string_of_puzzle_states_" + str(i) + ".csv"
        puzzle_state = np.genfromtxt(filename, delimiter=",")
        if puzzle_state.shape[0] == 48:
            puzzle_states.append(puzzle_state.reshape((8,6,12)))

            filename = "collect_data/ground_truth/list_of_moves_" + str(i) + ".csv"
            puzzle_class = np.genfromtxt(filename, delimiter=",")
            classes.append(puzzle_class)

    return np.array(puzzle_states), np.array(classes)

def get_batch(puzzle_states, classes, index):
    if index > puzzle_states.shape[0] - batch_size:
        index = 0

    puzzle_batch = puzzle_states[index,1:8,:,:]
    puzzle_batch = puzzle_batch.reshape((7,6*12))
    classes =  np.rot90(np.identity(7))

    return puzzle_batch, classes

saver = tf.train.Saver()
index = 0
# Launch the graph
with tf.Session() as sess:
    sess.run(init)

    puzzle_states, classes = input_data()

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0.
        # Loop over all batches
        for i in range(batch_size):
            # pdb.set_trace()
            batch_x, batch_y = get_batch(puzzle_states, classes, index)
            index = index + 1
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                          y: batch_y})
            # Compute average loss
            avg_cost += c / puzzle_states.shape[0]
        # Display logs per epoch step
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", \
                "{:.9f}".format(avg_cost))
    print("Optimization Finished!")

    save_model = "heuristic.ckpt"
    saver.save(sess,save_model)

    pdb.set_trace()
    temp = batch_x[6].reshape((1,72))
    prediction = sess.run(tf.nn.sigmoid(pred), feed_dict={x: temp})

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({x: batch_x, y: batch_y}))
