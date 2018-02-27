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
        return tf.sigmoid(tf.matmul(prev_layer, weights) + biases)
   

    # Store layers weight & bias
    def activate(self, inputs):
        logger.info('activating for input %s' %(str(inputs),))
        outputs = Perceptron._session.run(self.pred, feed_dict={self.x: inputs})
        return outputs


    def get_dict(self):
        arr1 = tf.reshape(self.weights['h1'], [self.n_input*self.n_hidden_1]).eval(session=Perceptron._session)
        arr2 = tf.reshape(self.weights['out'],[self.n_hidden_1*self.n_output]).eval(session=Perceptron._session)
        weight_arr = numpy.append(arr1, arr2)
        biases_arr = numpy.append(self.biases['b1'].eval(session=Perceptron._session),self.biases['out'].eval(session=Perceptron._session))

        return {"weights":weight_arr, "biases":biases_arr}


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
        pass


    def __unicode__(self):
        return str(self.fitness)
