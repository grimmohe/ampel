'''
A Multilayer Perceptron implementation example using TensorFlow library.

'''
import copy
import tensorflow as tf
import numpy
import logging
import sys
logger = logging.getLogger('percp')
import time
import random


class Perceptron(object):

    _session = tf.Session()
    __tensor_cache = {}
    _ops = {
        "copy": lambda obj1, obj2, factor: tf.assign(obj1, obj2),
        "cross": lambda obj1, obj2, factor: tf.assign(obj1, tf.divide(tf.add(obj1, obj2), 2)),
        "mutate": lambda obj1, obj2, factor: tf.assign(obj1, tf.add(obj1, tf.random_uniform(shape=tf.shape(obj1), minval=factor*-1, maxval=factor)))
    }


    def __init__(self, n_input, n_output):
        self.n_input = n_input
        self.n_output = n_output
        self.fitness = sys.maxsize
        self.x = tf.placeholder('float', [None, self.n_input])
        self.layers = {}
        self.pred = self._multilayer_perceptron()


    @staticmethod
    def init():
        Perceptron._session.run(tf.global_variables_initializer())


    @staticmethod
    def log_tensor_object_counts():
        logger.info("tf operations %s", len(tf.get_default_graph().get_operations()))


    @staticmethod
    def _get_tensor(name, obj1, obj2=None, factor=0):
        tensor = Perceptron.__tensor_cache.get((name, obj1, obj2))
        if tensor == None:
            tensor = Perceptron._ops[name](obj1, obj2, factor)
            Perceptron.__tensor_cache[(name, obj1, obj2)] = tensor
        return tensor


    def _multilayer_perceptron(self):
        pass


    def set_fitness(self, points):
        self.fitness = points


    # Store layers weight & bias
    def activate(self, inputs):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('activating for input %s' %(str(inputs),))
        outputs = Perceptron._session.run(self.pred, feed_dict={self.x: inputs})
        return outputs


    def copy(self, other):
        for layer in self.layers:
            Perceptron._get_tensor("copy", self.layers[layer], other.layers[layer]).eval(session=Perceptron._session)


    def cross(self, other):
        for layer in self.layers:
            self._cross(self.layers[layer], other.layers[layer])


    def _cross(self, own, other):
        Perceptron._get_tensor("cross", own, other).eval(session=Perceptron._session)


    def mutate(self, factor=0.2):
        for layer in self.layers:
            self._mutate(self.layers[layer], factor)


    def _mutate(self, layer, factor):
        Perceptron._get_tensor("mutate", layer, factor=factor).eval(session=self._session)


    def __unicode__(self):
        return str(self.fitness)


class Perceptron_1Layer(Perceptron):

    def __init__(self, n_input, n_hidden_1, n_output):
        self.n_hidden_1 = n_hidden_1
        Perceptron.__init__(self,n_input, n_output)

     # Create model
    def _multilayer_perceptron(self):

        self.layers['h1'] = tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1]))
        self.layers['ol'] = tf.Variable(tf.random_normal([self.n_hidden_1, self.n_output]))
        self.layers['b1'] = tf.Variable(tf.random_normal([self.n_hidden_1]))
        self.layers['ob'] = tf.Variable(tf.random_normal([self.n_output]))

        layer_1 =  tf.sigmoid(tf.add(tf.matmul(self.x, self.layers['h1']), self.layers['b1']))
        out = tf.sigmoid(tf.add(tf.matmul(layer_1,  self.layers['ol']), self.layers['ob']))

        return out

class Perceptron_2Layer(Perceptron):

    def __init__(self, n_input, n_hidden_1, n_hidden_2, n_output):
        self.n_hidden_1 = n_hidden_1
        self.n_hidden_2 = n_hidden_2
        Perceptron.__init__(self,n_input, n_output)

    # Create model
    def _multilayer_perceptron(self):

        self.layers['h1'] = tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1]))
        self.layers['h2'] = tf.Variable(tf.random_normal([self.n_hidden_1, self.n_hidden_2]))
        self.layers['ol'] = tf.Variable(tf.random_normal([self.n_hidden_2, self.n_output]))
        
        self.layers['b1'] = tf.Variable(tf.random_normal([self.n_hidden_1]))
        self.layers['b2'] = tf.Variable(tf.random_normal([self.n_hidden_2]))
        self.layers['ob'] = tf.Variable(tf.random_normal([self.n_output]))

        layer_1 =  tf.tanh(tf.add(tf.matmul(self.x, self.layers['h1']), self.layers['b1']))
        layer_2 =  tf.tanh(tf.add(tf.matmul(layer_1, self.layers['h2']), self.layers['b2']))
        out = tf.add(tf.matmul(layer_2,  self.layers['ol']), self.layers['ob'])
        
        return out

