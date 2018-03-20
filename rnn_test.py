import tensorflow as tf
import sys

n_input = 2
n_hidden_1 = 2
n_output = 2

sess = tf.Session()

with sess.as_default():

    x = tf.placeholder('float', [None, n_input])

    hidden1 = tf.Variable(tf.ones([n_input, n_hidden_1]))
    hidden1_mem = tf.Variable(tf.ones([1, n_hidden_1]))
    output = tf.Variable(tf.ones([n_hidden_1, n_output]))
    outputbias = tf.Variable(tf.ones([n_output]))

    op = tf.matmul(x, hidden1)
    mem =  tf.assign(hidden1_mem, tf.add(op, hidden1_mem))
    out = tf.add(tf.add(mem,  output), outputbias)

    sess.run(tf.global_variables_initializer())

    for _ in range(5):
        print("h", hidden1.eval())
        print("m", hidden1_mem.eval())
        print("o", sess.run(out, feed_dict={x: [[2, 1]]}))

