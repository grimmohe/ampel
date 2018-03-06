'''
A Multilayer Perceptron implementation example using TensorFlow library.

'''
import copy
import tensorflow as tf
import numpy
import logging
logger = logging.getLogger('percp')
import time
import random


class Perceptron(object):

    _session = tf.Session()

    def __init__(self, n_input, n_hidden_1, n_output):
        self.n_input = n_input
        self.n_hidden_1 = n_hidden_1
        self.n_output = n_output
        self.fitness = 0
        self.weights = {
            'h1': tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1])),
            'out': tf.Variable(tf.random_normal([self.n_hidden_1, self.n_output]))
        }
        self.biases = {
            'b1': tf.Variable(tf.random_normal([self.n_hidden_1])),
            'out': tf.Variable(tf.random_normal([self.n_output]))
        }
        self.x = tf.placeholder('float', [None, self.n_input])
        self.pred = self._multilayer_perceptron(self.x, self.weights, self.biases)


    @staticmethod
    def init():
        Perceptron._session.run(tf.global_variables_initializer())


    def set_fitness(self, points):
        self.fitness = points


     # Create model
    def _multilayer_perceptron(self, input, weights, biases):
        layer_1 =  self._append(input, weights['h1'], biases['b1'])
        out = self._append(layer_1,  weights['out'], biases['out'])
        return out


    def _append(self, prev_layer, weights, biases):
        return tf.sigmoid(tf.add(tf.matmul(prev_layer, weights), biases))
   

    # Store layers weight & bias
    def activate(self, inputs):
        logger.info('activating for input %s' %(str(inputs),))
        outputs = Perceptron._session.run(self.pred, feed_dict={self.x: inputs})
        return outputs


    def copy(self, other):
        for key in self.weights:
            tf.assign(self.weights[key], other.weights[key]).eval(session=Perceptron._session)
        for key in self.biases:
            tf.assign(self.biases[key], other.biases[key]).eval(session=Perceptron._session)


    def cross(self, other):
        for key in self.biases:
            self._cross(self.biases[key], other.biases[key])
        for key in self.weights:
            self._cross(self.weights[key], other.weights[key])


    def _cross(self, own, other):
        tf.assign(own, tf.divide(tf.add(own, other), 2)).eval(session=Perceptron._session)


    def mutate(self, factor=0.2):
        for key in self.weights:
            self._mutate(self.weights[key], factor)
        for key in self.biases:
            self._mutate(self.biases[key], factor)

    def _gaussian_noise_layer(self, input_layer, factor):
        noise = tf.random_uniform(shape=tf.shape(input_layer), minval=factor*-1, maxval=factor)
        print("noise", noise.eval(session=Perceptron._session))
        return tf.add(input_layer, noise)

    def _mutate(self, layer, factor):
        noise = self._gaussian_noise_layer(layer, factor)
        tf.assign(layer, noise).eval(session=self._session)

    def __unicode__(self):
        return str(self.fitness)
