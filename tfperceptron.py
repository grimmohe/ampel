'''
A Multilayer Perceptron implementation example using TensorFlow library.

'''
import copy
import tensorflow as tf
import numpy
import logging
logger = logging.getLogger('percp')
import time


class Perceptron(object):

    def __init__(self, n_input, n_hidden_1, n_output):
        self.n_input = n_input
        self.n_hidden_1 = n_hidden_1
        self.n_output = n_output
        self.sess = None
        self.fitness = 0
        self.initialized = False
        self.weights = {'h1':None,  'out': None}
        self.biases = {'b1':None,  'out':None}
        self.fitness = 0
        self.weights_arr = []
        self.biases_arr = []
        
    def set_fitness(self, points):
        self.fitness = points

     # Create model
    def multilayer_perceptron(self, input, weights, biases):
        layer_1 =  self._append(input, weights['h1'], biases['b1'])
        out = self._append(layer_1,  weights['out'], biases['out'])

        return out

    def _append(self, prev_layer, weights, biases):
        return tf.sigmoid(tf.matmul(prev_layer, weights) + biases)
   
    # tf Graph input
    def init1(self):
        self.weights = {
        'h1': tf.Variable(tf.random_normal([self.n_input, self.n_hidden_1])),
        
        'out': tf.Variable(tf.random_normal([self.n_hidden_1, self.n_output]))
        }
        self.biases = {
            'b1': tf.Variable(tf.random_normal([self.n_hidden_1])),
           
            'out': tf.Variable(tf.random_normal([self.n_output]))
        }
        self.x = tf.placeholder('float', [None, self.n_input])
        self.pred = self.multilayer_perceptron(self.x, self.weights, self.biases)
        self.sess = tf.Session()
        self.init = tf.initialize_all_variables()
        self.sess.run(self.init)
        self.get_dict()
        self.initialized = True
   
    # Store layers weight & bias
    def activate(self,inputs):
        logger.info('activating for input %s' %(str(inputs),))
        if self.initialized is False:
            self.init1()
        outputs = self.sess.run(self.pred, feed_dict={self.x: inputs})
        return outputs

    def get_dict(self):
        arr1 = tf.reshape(self.weights['h1'], [self.n_input*self.n_hidden_1]).eval(session=self.sess)
        arr2 = tf.reshape(self.weights['out'],[self.n_hidden_1*self.n_output]).eval(session=self.sess)
        weight_arr = numpy.append(arr1, arr2)
        biases_arr = numpy.append(self.biases['b1'].eval(session=self.sess),self.biases['out'].eval(session=self.sess))
        self.weights_arr = weight_arr
        self.biases_arr = biases_arr
        self.as_dict = {"weights":weight_arr,"biases":biases_arr}

        return self.as_dict

    def reload(self):
        weights_arr = self.as_dict['weights']
        biases_arr = self.as_dict['biases']
        dim1 = self.n_input*self.n_hidden_1
        h1 = tf.convert_to_tensor(weights_arr[:dim1])
        out = tf.convert_to_tensor(weights_arr[dim1:])

        self.weights['h1'] = tf.reshape(h1,[self.n_input,self.n_hidden_1])
        self.weights['out'] = tf.reshape(out,[self.n_hidden_1,self.n_output])
        self.biases['b1'] = tf.convert_to_tensor(biases_arr[:self.n_hidden_1])
        self.biases['out'] = tf.convert_to_tensor(biases_arr[self.n_hidden_1:])
        self.x = tf.placeholder('float', [None, self.n_input])
        self.sess = tf.Session()
        self.init = tf.initialize_all_variables()
        self.sess.run(self.init)
        self.pred = self.multilayer_perceptron(self.x, self.weights, self.biases)
        self.initialized = True


    def copy(self):
        d = copy.deepcopy(self.as_dict)
        p = Perceptron(self.n_input,self.n_hidden_1,self.n_output)
        p.as_dict = d
        return p

    def __unicode__(self):
        return str(self.fitness)
